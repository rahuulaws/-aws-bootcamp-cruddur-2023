import os
import re
import sys
from psycopg_pool import ConnectionPool
from flask import current_app as app


class Db:
    def __init__(self):
        # Get the CONNECTION_URL form environment and pass it to ConnctionPool imported from psycopg_pool
        connection_url = os.getenv("CONNECTION_URL")
        # print("Connection URL is: " + connection_url)
        self.pool = ConnectionPool(connection_url)

#################################
#################################
# Class Helper functions -- Begin
#################################
#################################
    def template(self, *args):
        # Args cam be any length but are a tuple, the last argument of args will be the file name
        # From which DB SQL need to be loaded
        pathing = list((app.root_path, 'db', 'sql', ) + args)
        pathing[-1] = pathing[-1] + ".sql"
        template_path = os.path.join(*pathing)
        # Coloured printing
        green = '\033[92m'
        no_color = '\033[0m'
        print("\n")
        print(f'{green} Load SQL Template: {template_path} {no_color}')
        with open(template_path, 'r') as f:
            template_content = f.read()
        return template_content

    # Function to print SQL Parameters in colour
    def print_params(self, params):
        blue = '\033[94m'
        no_color = '\033[0m'
        print(f'{blue} SQL Params:{no_color}')
        for key, value in params.items():
            print(key, ":", value)

    # Function to print SQL in colour
    def print_sql(self, title, sql,params={}):
        cyan = '\033[96m'
        no_color = '\033[0m'
        print(f'{cyan} SQL STATEMENT-[{title}]------{no_color}')
        print(sql,params)

#################################
#################################
# Class Helper functions -- End
#################################
#################################

#################################
#################################
# Class Main functionality -- Begin
#################################
#################################
    # Main Commit function to execute a QUERY
    def query_commit(self, sql, params={}, verbose=True):
        if verbose:
            self.print_sql('commit with returning', sql, params)
        # we want to commit data such as an insert
        # be sure to check for RETURNING in all uppercases
        pattern = r"\bRETURNING\b"
        is_returning_id = re.search(pattern, sql)

        try:
            with self.pool.connection() as conn:
                cur = conn.cursor()
                cur.execute(sql, params)
                if is_returning_id:
                    returning_id = cur.fetchone()[0]
                conn.commit()
                if is_returning_id:
                    return returning_id
        except Exception as err:
            self.print_sql_err(err)

    # when we want to return a json object

    def query_array_json(self, sql, params={}, verbose=True):
        if verbose:
            self.print_sql('array', sql, params)

        wrapped_sql = self.query_wrap_array(sql)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                json = cur.fetchone()
                return json[0]

    # When we want to return an array of json objects
    def query_object_json(self, sql, params={}, verbose=True):
        if verbose:
            self.print_sql('json', sql, params)
            self.print_params(params)

        wrapped_sql = self.query_wrap_object(sql)

        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                json = cur.fetchone()
                if json == None:
                   return "{}"
                   
                else:
                    return json[0]
    def query_value(self, sql, params={}, verbose=True):
        if verbose:
            self.print_sql('value', sql, params)
            
        with self.pool.connection() as conn:
             with conn.cursor() as cur:
                  cur.execute(sql,params)
                  json = cur.fetchone()

                  if json is not None:
                    return json[0]
                  else:
                    return None

    def query_wrap_object(self, template):
        sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
        return sql

    def query_wrap_array(self, template):
        sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
        return sql

    def print_sql_err(self, err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()
        # get the line number when exception occured
        line_num = traceback.tb_lineno

        # print the connect() error
        print("\npsycopg ERROR:", err, "on line number:", line_num)
        print("psycopg traceback:", traceback, "-- type:", err_type)

        # print the pgcode and pgerror exceptions
        # print("pgerror: ", err.pgerror)
        # print("pgcode: ", err.pgcode, "\n")
#################################
#################################
# Class Main functionality -- End
#################################
#################################


db = Db()