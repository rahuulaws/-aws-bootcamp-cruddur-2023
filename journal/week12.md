# Week 12 — Week X 

### Sync tool for static website hosting

### Context and Background 

 - We have used CFN Template to provision the following resurces in AWS under the Static Website Hosting as a Frontend activity.

     - CloudFront Distribution (https://di38zz9ba2r5u.cloudfront.net) mapped to Public S3 Bucket : cloudnoww.com as an Origin
     - S3 Bucket for www : www.cloudnoww.com 
     - S3 Bucket for naked domain : cloudnoww.com
     - RootBucketDomain : cloudnoww.com ,which is mapped to the above Cloudfront distribution (https://di38zz9ba2r5u.cloudfront.net)
     - WwwBucketDomain : www.cloudnoww.com ,which is mapped to the above Cloudfront distribution (https://di38zz9ba2r5u.cloudfront.net)
     - Bucket Policy                
                 
 - We now need a way to sync any changes that are made to the frontend files to the Public s3 Bucket - cloudnoww.com which is the origin for the Cloudfront distribution. 
 - Sync Tool for static website hosting is the antidote for achieving the challenge of moving changes in frontend files to S3. 
         
 - In view of the above, we started off by creating a bash script file - static build. Details as below. It is executed manually by changing directory in gitpod terminal to the front-react-js path.
 - The error free bash script is run in the following path ./bin/frontend/static-build
        #! /usr/bin/bash

        ABS_PATH=$(readlink -f "$0")
        FRONTEND_PATH=$(dirname $ABS_PATH)
        BIN_PATH=$(dirname $FRONTEND_PATH)
        PROJECT_PATH=$(dirname $BIN_PATH)
        FRONTEND_REACT_JS_PATH="$PROJECT_PATH/frontend-react-js"

        cd $FRONTEND_REACT_JS_PATH

        REACT_APP_BACKEND_URL="https://api.cloudnoww.com" \
        REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
        REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
        REACT_APP_AWS_USER_POOLS_ID="us-east-1_1P8HDMxzW" \
        REACT_APP_CLIENT_ID="6vd6cd42sutct7v0m6e3udljri" \
        npm run build
  
     
 - After the static build is completed. The content of the build folder is zipped by using the command : zip -r build.zip build/ and uploaded in the Public S3 Bucket : cloudnoww.com
  
  ![Cloudnoww com-S3Bucket](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/2be98765-8cfa-4b5e-9a38-d20911d03f73)

 -  We see the application on accessing www.cloudnoww.com through any web browser. 

 ![S3 signin](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/16882b1f-8dc3-414b-aab4-2deb784b3642)

 
### Installing the sync tool to sync the changes made in frontend application to the Public s3 bucket - cloudnoww.com

- We create a new bash script file in the path  ./bin/frontend/sync.
- Install the aws_s3_website_sync by using gem install aws_s3_website_sync, which installs the package aws_s3_website_sync required in the sync script. 
- temp directory is created along with a file .keep. The command : git add -f temp/.keep - is used for the file to be added to the repo in gitpod. 
- File is created for sync-env to specify the env vars in the folder erb  ./erb/sync.env.erb  for the bash script file  ./bin/frontend/sync

        SYNC_S3_BUCKET=cloudnoww.com
        SYNC_CLOUDFRONT_DISTRUBTION_ID=ERY3XWMWSJ69A
        SYNC_BUILD_DIR=<%= ENV['THEIA_WORKSPACE_ROOT'] %>/frontend-react-js/build
        SYNC_OUTPUT_CHANGESET_PATH=<%=  ENV['THEIA_WORKSPACE_ROOT'] %>/tmp/changeset.json
        SYNC_AUTO_APPROVE=false
  
 - The bash script file ./bin/frontend/generate-env is modified to generate the env var for the files namely : frontend-react-js.env.erb and sync.env.erb
 - The command ./bin/frontend/generate-env is used to generate both the env files for frontend-react-js. 
 - The package dotenv is installed for uploading the env files. 'gem install dotenv
 - The bash script file '././bin/frontend/sync is executed to generate the file of changes that needs to be pushed to the s3 bucket through the cloudfront invalidation.

### Testing the sync tool

- An exclaimation mark is added after About ! in the file - DesktopSidebar.js below,  which is part of the frontend application. 

                   return (
                            <section>
                              <Search />
                              {trending}
                              {suggested}
                              {join}
                              <footer>
                                 <a href="/about">About!</a>
                                
                                 <a href="/terms-of-service">Terms of Service</a>
                                
                                 <a href="/privacy-policy">Privacy Policy</a>
                             </footer>
                           </section>
                                              

- The bash script file in the path  ./bin/frontend/static-build is executed and post the build, the sync file on the path  ./bin/frontend/sync is executed to check whether the above changes are made or not
  to the web page. 
- An invalidation file is generated on the cloudfront as shared below. 

![CloudfrontInvalidation](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/d23d7a6f-50b9-4d99-9268-14bd3215e55f)


- Use any browser to access cloudnoww.com to find ot whether the changes made in the DesktopSidebar.js file are reflected in the frontend web page. 

![Exclamation](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/c3889c26-a18d-426f-b934-92e5646c5808)


### Using Github actions to build and deploy the sync

- A folder is created at the rrot level ./github/workflows with a new file - sync.yml with the path ./github/workflows/sync.yaml
  
  ![Github](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/47e76f7f-3a2f-475f-ad54-bb9f9cb5a228)


- Gemfile is created under  .github for installing required dependancies like dotenv, aws_s3_website_sync and rake with the command : bundle update --bundler
     
                 source 'https://rubygems.org'

                 git_source(:github) do |repo_name|
                 repo_name = "#{repo_name}/#{repo_name}" unless repo_name.include?("/")
                 "https://github.com/#{repo_name}.git"
                 end
                 gem 'rake'
                 gem 'aws_s3_website_sync', tag: '1.0.1'
                 gem 'dotenv', groups: [:development, :test]

 - it will generate the gemfile.lock file
 - Create a rake file under the '.github' folder so that any changes in the files of frontend-react-js are synced to the Public S3 bucker : cloudnoww.com 
 
                  require 'aws_s3_website_sync'
                  require 'dotenv'

                  task :sync do
                    puts "sync =="
                    AwsS3WebsiteSync::Runner.run(
                      aws_access_key_id:     ENV["AWS_ACCESS_KEY_ID"],
                      aws_secret_access_key: ENV["AWS_SECRET_ACCESS_KEY"],
                      aws_default_region:    ENV["AWS_DEFAULT_REGION"],
                      s3_bucket:             ENV["S3_BUCKET"],
                      distribution_id:       ENV["CLOUDFRONT_DISTRUBTION_ID"],
                      build_dir:             ENV["BUILD_DIR"],
                      output_changset_path:  ENV["OUTPUT_CHANGESET_PATH"],
                      auto_approve:          ENV["AUTO_APPROVE"],
                      silent: "ignore,no_change",
                      ignore_files: [
                        'stylesheets/index',
                        'android-chrome-192x192.png',
                        'android-chrome-256x256.png',
                        'apple-touch-icon-precomposed.png',
                        'apple-touch-icon.png',
                        'site.webmanifest',
                        'error.html',
                        'favicon-16x16.png',
                        'favicon-32x32.png',
                        'favicon.ico',
                        'robots.txt',
                        'safari-pinned-tab.svg'
                      ]
                    )
                  end
 - A Cloudformation stack is used for creating resources like  IAM role, OIDCProvider in the aws using the bash script file at the path bash script file to provision the changeset stack aws/cfn/sync/template.yaml.
 - Config.toml file which has key configuration details such as the name of the stack - CrdSyncRole, region of deployment, S3 Bucketname details along with the following parameters are referenced by the CFN template.
                  
                  GitHubOrg = 'rahuulaws'
                  RepositoryName = '-aws-bootcamp-cruddur-2023'
                  OIDCProviderArn = ''
    
                 
  - Bash script kept under the path ./bin/cfn/sync is run which deploys the CFN template with aws cli command.
   
   ![CFNCrdSyncrole](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/63c1d2f7-a623-4be3-ad8b-3e072ce54033)

  
  ![CFNCrdSyncroleResources](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/beb839e5-9e37-4091-9af5-76a8b717f070)


  
  ![CFNCrdSyncroleParameters](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/45b77745-95bd-41c2-8a98-b9ea7d6bee73)

  
  ![CFNCrdSyncRoleOutputs](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/629d544b-a846-4d83-8b37-92c39b59572e)  
   

 - Under the IAM Service using the aws console, one can see the CrdSyncRole to which we add inline permissions as give below
 
  ![IAMCrdSyncRole](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/d4994f2d-b56d-4793-a665-23aea18cc5e0)
  
 - The CrdSync Role ARN :  arn:aws:iam::881652387149:role/CrdSyncRole-Role-L7O62EBAFN5H is copied in the  sync.yaml file at the path ./github/workflows/sync.yaml 
 - Documents which were referenced are : github actions github_action_configure-aws-credentials

### Reconnect Database and Post Confirmation Lambda

  - We have so far synced the frontend files to the Public s3 Bucket - cloudnoww.com which is the origin for the Cloudfront distribution. 
  - Now we need to connect the RDS Database - cruddur-cfninstance, that was created through the CFN Template.
  - The CFN CICD is edited to take serviceName:backend-flask and we also take a decision on using a cross- stack name. 
  - Execute the CFN CICD by running the bash script at the path . /bin/cfn/cicd and post which Execute the CFN service stack by running the bash script at the path ./bin/cfn/service. 
  - It is a good practice to test locally and it is done by editing the docker-compose.yaml file to point to  - Dockerfile.prod for the build in service: backend-flask
  - After starting the application by doing docker compose up, the backend-flask is checked in any web browser through api/activities/home
  - The following error message is seen.
  
   ![InternalServerError](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/4c4e03c3-835b-4954-ad45-defe6c3e3083)

 
  - We now need to build the backend-flask docker file pointing to Dockerfile.prod through the bash script at the path ./bin/backend/build
           
           
             #! /usr/bin/bash

            ABS_PATH=$(readlink -f "$0")
            BACKEND_PATH=$(dirname $ABS_PATH)
            BIN_PATH=$(dirname $BACKEND_PATH)
            PROJECT_PATH=$(dirname $BIN_PATH)
            BACKEND_FLASK_PATH="$PROJECT_PATH/backend-flask"

            docker build \
            -f "$BACKEND_FLASK_PATH/Dockerfile.prod" \
            -t backend-flask-prod \
            "$BACKEND_FLASK_PATH/."
 
     - After pushing the new backend-flask image to ECR, we execute CFN service by running the bash script at the path ./bin/cfn/service and ensuring the ECS : backend-flask service is working fine. 
     - We check the backend-flask : api.cloudnoww.com/api/activities/home in any web browser and observe the following error.
 
       ![upstreamrequest](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/09193106-d7ed-44c0-a989-7f31c1a3eefe)
   
     - We need to ensure that the prod_connection url is reaching out to the new rds db and not the one that was created earlier. The prod_connection url will reflect as follows
  
       ![PRODCONNECTIONURL](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/e55a7bd4-fc4f-4016-bccb-8e64fd743183)

    - The Security Group for New RDS - cruddur-cfninstance, is edited to allow Inbound access for Gitpod terminal even on new workspace being used by using curl ifconfig.me and ./bin/rds/update-sg-rule. 
    - Now we connect to the New RDS DB - cruddur-cfninstance, using ./bin/db/connect prod, followed by schema-load by using the bash script at the path running ./bin/db/schema-load prod
    - Run the migrate script. CONNECTION_URL=$PROD_CONNECTION_URL ./bin/db/migrate ( this is done to override the connection url to prod connection url)
    - Redeployed the edited CFN Frontend stack through the bash script at the path ./bin/cfn/frontend to address the errors that came up. 
  
 ### Modify the lambda function cruddur-post-confirmation to connect to the New RDS DB : cruddur-cfninstance
   - The Lambda Function - cruddur-post-confirmation is invoked through the AWS Cognito which is used when a new user sign up or an existing user sign in to the web application. 
   - The following change are implemented in the Lambda Function - cruddur-post-confirmation so that it connects to the New RDS DB : cruddur-cfninstance.
      - Edited the connection url in env var to cruddur-cfninstance.
      
       ![LambdaPostConfirmationEnvr](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/cacd7eb8-2a8b-4dbf-96c4-ba4615a8b9ab)

      - A New SG : CognitoLambdaSG is created containing ONLY an Outbound Rule with ALLTRAFFIC 0.0.0.0/0 and no rules on Inbound and attach the Lambda Function to the New VPC : CrdNetVPC created through CFN so
       that Lambda Function can access the New RDS DB : cruddur-cfninstance, which is also attached to VPC : CrdNetVPC.
       
       ![LambdaPostConfirmationVPC](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/82cbd8ac-0564-414a-8749-6ec3c69be023)

           
      - The Lambda code is modified since the data insertion into RDS is not happening. The Key change amongst others being editing : cur.execute(sql,*params) to cur.execute(sql,params).
  
                                      import json
                                      import psycopg2
                                      import os

                                      def lambda_handler(event, context):
                                          user = event['request']['userAttributes']
                                          print('userAttributes')
                                          print(user)
                                          user_display_name = user['name']
                                          user_email = user['email']
                                          user_handle = user['preferred_username']
                                          cognito_user_id = user['sub']

                                          conn = None

                                          try:
                                              print('entered-try')
                                              sql = """
                                                  INSERT INTO public.users (
                                                      display_name,
                                                      email,
                                                      handle,
                                                      cognito_user_id
                                                  )
                                                  VALUES (
                                                      %(display_name)s,
                                                      %(email)s,
                                                      %(handle)s,
                                                      %(cognito_user_id)s
                                                  )
                                              """
                                              print('SQL Statement ----')
                                              print(sql)

                                              conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
                                              cur = conn.cursor()
                                              params = {
                                                  'display_name': user_display_name,
                                                  'email': user_email,
                                                  'handle': user_handle,
                                                  'cognito_user_id': cognito_user_id
                                              }
                                              cur.execute(sql, params) <--------------------- this was changed
                                              conn.commit()

                                          except (Exception, psycopg2.DatabaseError) as error:
                                              print('error:')
                                              print(error)

                                          finally:
                                              if conn is not None:
                                                  cur.close()
                                                  conn.close()
                                                  print('Database connection closed.')
                                              else:
                                                  print('No connection to close.')

                                          return event

  
  ### Crudding !! 

  ![Afterlogin](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/2df94bc4-e12e-48b4-8157-076dc859c617)


  
  ### Use CORS for Service
  
  - The parameters - EnvFrontendUrl = 'https://cloudnoww.com' and  EnvBackendUrl = 'https://api.cloudnoww.com' are passed to the CFN Service stack by updating the config.tom at the path ./aws/cfn/service/config.toml
  - Subsequently the bashscript is updated at the path ./bin/cfn/service so that the parameters can be passed to the CFN Service stack

                                      #! /usr/bin/env bash
                                      set -e # stop the execution of the script if it fails

                                      CFN_PATH="/workspace/-aws-bootcamp-cruddur-2023/aws/cfn/service/template.yaml"
                                      CONFIG_PATH="/workspace/-aws-bootcamp-cruddur-2023/aws/cfn/service/config.toml"

                                      echo $CFN_PATH

                                      cfn-lint $CFN_PATH

                                      BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
                                      REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
                                      STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
                                      PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)


                                      aws cloudformation deploy \
                                        --stack-name $STACK_NAME \
                                        --s3-bucket $BUCKET \
                                        --s3-prefix backend-service \
                                        --region $REGION \
                                        --template-file "$CFN_PATH" \
                                        --no-execute-changeset \
                                        --tags group=cruddur-backend-flask \
                                        --parameter-overrides $PARAMETERS \
                                        --capabilities CAPABILITY_NAMED_IAM

  - The Service stack is executed again by running the script at the path ./bin/cfn/service and one can now se the envr being passed in the parameters.

    ![BackebdFlaskEnvr](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/400fd861-34e5-4778-b60b-ee82d1c59866)


 ### CICD Pipeline and Create Activity
 
 - We create another cognito user by signing up in the application and post which we make a Crud message with the new cognito user.
 - The Crud messsage by the new cognito user is not reflecting with the name of the new cognito user but of an hardcoded vaue that must be changed in Activitiyform.js file.
 - We also conduct a test with the new cognito user in the local development environment by connecting with local postgres db and the same is done by pointing Dockerfile to local db by making relevant changes 
   in the docker-compose.yaml file and get it into run by doing docker compose up.
 - We seed the data into local db by executing the file at the path ./bin/db/setup and we update the cognito_user_id by running the script at the path ./bin/db/update_cognito_user_ids 
 - Changes needed to be done in the Activityform.js to pass the bearer token so that message sent by the new cognito user reflects under their name. 
  
  ![Newuser](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/207b80ac-65df-4142-b70c-49e2367347e1)
  
  - We want to check now whether the changes can be rolled out by using the CICD pipeline created by CFN Template.
  - A pull request is made in Github by merging GitHubBranch : Production into Main branch of Github which builds and deploy through the CICD workflow created by CFN Template which is listening into the changes in my 
    Github repo - rahuulaws/-aws-bootcamp-cruddur-2023.
  - Errors encountered during the CICD run are addressed by doing the following
        
        - changing the parameters :  GithubRepo = 'rahuulaws/-aws-bootcamp-cruddur-2023' in config.toml at the path aws/cfn/cicd/config.toml
        - changing the code build name in the codebuild.yaml file on the path aws/cfn/cicd/nested/codebuild.yaml and the template.yaml file on the path aws/cfn/cicd/template.yaml
   
   ![cicd](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/1ec45ee0-208e-4c96-a726-536f528db4b3)
   
   
   ![Screenshot 2023-05-20 234459](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/61c603df-d31c-4dd2-8d1c-010ffd5b7549) 
  
  
   ![Homepage](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/001d0d21-1124-46b5-b5b1-905e2209d83c)

### Refactor JWT to use a decorator

 - The replyform.js is modified so that the reply box for a Crud message closes when it is clicked outside of the box, based on the on the reply_popup onclick

   ![Reply](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/293d0f00-60ba-479a-b24f-ab163b259187)
   
   ![ReplyMessage](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/2c2c0f59-5bc1-486a-8a25-2083c7581aec)

 - We decide to use Decorators as a design pattern, which are explained below. Please note that I have used ChatGPT for the below explaination.
 
     - Decorators provide a flexible and modular way to extend or modify the functionality of existing code without the need to change its implementation directly. 
     - They promote code reuse and separation of concerns, making the code more maintainable and easier to understand.
     - To summarize, decorators are like add-ons or wrappers that allow us to modify or enhance the behavior of existing objects or functions without modifying their code directly
          
 - We create a decorator for JWT verification by changing the code in app.py at the path ./backend-flask/app.py and backend-flask/lib/cognito_jwt_token.py.
 - Post the change, the web application is checked to find out whether it is working properly or not. 
   
   ![PostDecorator](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/3d821979-30ee-4118-93d7-fb4524180785)


### Refactor AppPy

- We decide to Refactor the app.py and also use chaining which is explained below. Please note that I have used ChatGPT for the below explaination.
 
     - Refactoring mean making changes to an existing code to improve its structure, readability, and maintainability without altering its functionality. 
     - Refactoring helps make our code cleaner, easier to understand, and easier to modify in the future.
         
     - Chaining in Python refers to the practice of connecting multiple operations or methods together in a sequence and makes our code more concise and readable because it allows us to 
       perform multiple operations on a single line
     - It allows us to perform a series of actions on an object or data by applying one operation after another. 
     - It's like a chain of actions, where the output of one action becomes the input for the next one.
     
- We create seperate python files for different functionalities/operations performed by different services such as cloudwatch (cloudwatch.py), xray(xray.py), rollbar(rollbar.py), honeycomb(homeycomb.py), 
  cloudwatch(cloudwatch.py) and cors(cors.py).
- We ensured all the errors are fixed and checked the app is working properly. 
- We also made changes in the notifications.py code to ensure that notifications page is aligned with the other pages in terms of the login details.


![notification](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/6b7d765e-aea5-4772-9dad-044de57cc57e)

  
![Home](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/edad6c9a-c97c-4889-a3ac-917be768cb7e)


### Refactor Flask Routes

- We decide to Refactor the "Routes" in app.py and the meaning of "Routes" in contect of Flask application is explained below. Please note that I have used ChatGPT for the below explaination.
 
   - In Flask applications, routes define the different web pages or URLs that users can visit. Think of routes as a map that tells our Flask application how to handle incoming requests and what content to display
      to the user
   - Each route corresponds to a specific URL or path, such as "/home" or "/contact". When a user enters a URL in their web browser, Flask uses the routes to determine which code or function should be executed to 
      generate the appropriate response.
   - Routes serve the purpose of mapping URLs to specific actions or functions in our Flask application. They help organize and structure our web application by defining the different pages or functionality available 
      to users. 
   - Refactoring "Routes" involves making changes to the existing route definitions to improve the structure, readability, or maintainability of our code.
  
- In our case, we have refactored the " Routes" by creating seperate python files for users.py, general.py, messages.py and activities.py which are referenced in the app.py through an import function as below.

     - import routes.general
     - import routes.activities
     - import routes.users
     - import routes.messages


### Replies Feature in the App

- When we do an inline reply to ur own message like below, we cant do it.

![Reply](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/6693a16e-f40c-449c-a82a-4cf6ba639175)

- We get an error message - "invalid input syntax for type integer" due to "reply_to_activitiy_uuid being" set as Integer in schema.sql
               
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                DROP TABLE IF EXISTS public.users;
                DROP TABLE IF EXISTS public.activities;
                CREATE TABLE IF NOT EXISTS public.schema_information (
                id integer UNIQUE,
                last_successful_run text
                );
                INSERT INTO public.schema_information (id, last_successful_run)
                VALUES(1, '0')
                ON CONFLICT (id) DO NOTHING;
                CREATE TABLE public.users (
                uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                display_name text NOT NULL,
                handle text NOT NULL,
                email text NOT NULL,
                cognito_user_id text NOT NULL,
                created_at TIMESTAMP default current_timestamp NOT NULL
                );
                CREATE TABLE public.activities (
                uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_uuid UUID not null,
                message text NOT NULL,
                replies_count integer DEFAULT 0,
                reposts_count integer DEFAULT 0,
                likes_count integer DEFAULT 0,
                reply_to_activity_uuid integer, <----we need to run a migration to convert this columnn from integer to accept uuid
                expires_at TIMESTAMP,
                created_at TIMESTAMP default current_timestamp NOT NULL
                );
                     
- We run the command ./bin/generate/migration reply_activity_uuid_to_string, which generates the migration file wherein we populate the following script to do that change and Run migrate ./bin/db/migrate to 
  change the table with field "reply_to_activity_uuid" to convert type "integer" to "uuid"

  ![MigrationScript](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/6902cf6b-8fae-403c-a964-c30f3e2dc2f5)
  
  ![Before and after snap of integer and uuuid](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/4c534183-6fa8-44d4-99df-219d0963f0c3)
  
- We check by replying to our own message and make some changes in the Activityitem.css for the replies to go inline above the main message. The local postegres db is also checked

   ![replies_final](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/4f5cb4ab-bb23-423c-a905-f970f88fddb5)
  
- The local postegres db is also checked to see the inline message being relfected in the db. 

  ![Activities](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/9937ebf9-a5ce-40e3-b143-8130d7a1c769)


###  Refactor Error Handling and Fetch Requests

- We decide to display a default message on application and on each page after one is loggedin to convey that there are no errors.
- This is achieved by putting in conditional content on Activityfeed.js file and changes in Activityfeed.css for displaying it on the web application.

![Nothingtoseehereyet](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/3db63289-7390-4471-af59-24a8fe61b03f)

- We want our application to be user friendly and it should render out different error messages so that our users knows what has gone wrong and that gives an idea to them about what is expected of them.  
- The error handling has been improved through a new file : FormErroritem.js which is referrred by different files through import function and list of errors messages are as below.
      
![Error Hnadling](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/ce1de5ad-75e0-4249-82bb-390d5f711454)



###  Activity Show Page

- The activity of migration does not currently tell us whether it is successfull or not, but as a temporary measure we moved forward by making the following changes ( first dropping the exsting column and then
  adding a new column ) in the migrations file as below

 ![integertouuid](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/3bfac75a-6fd6-4828-a5d8-a17783a2d64f)

 ![inreply](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/36572584-54c3-4730-b23e-768322659d0d)


###  Cleanup Part 1

- We want to see data from another user on our application and so we need to seed data through the file - seed.sql by making the following additions and then login to the local postgres db : Cruddur , by using the 
  command at the path ./bin/db/connect and inserting manually the sql command that were added in the seed.sql as below
  

                     (SELECT uuid from public.users WHERE users.handle = 'altbrown' LIMIT 1),
                     'I am the other!',
                      current_timestamp + interval '10 day'

- After login to the application, we get to see the see data from two users on the " Home" page.

 
 ![Homepage1](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/a07f5d18-8df2-492b-9aae-b4ac8adcb950)


- Change is made to the file : ActivityShowPage.js on the path ./frontend-react-js/src/pages/ActivityShowPage.js so that status page shows "Crud" at the top instead of "Home" that w have been seeing so far. 
- Back Button Arrow is also added which when pressed takes us to the "Home" page of the application by making changes in the activityshowpage.js and activityshowpage.css. 
- Exact time is also rendered by making changes in the file : ActivityItem.js at the path ./frontend-react-js/src/components/ActivityItem.js
- The above 3 changes result in the below modifications.

  ![Timeline](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/af5d85a1-b71c-4075-b2eb-82987b70ef5a)


- We realize that our migration has not been successfull on checking our local db -cruddur where the "reply_to_activitiy_uuid" still reflects as type " Integer" instead of "uuid"
- Currently we do not know whether the migration has failed or is succesfull, since it currently does not tell us about the outcome and we have to once again run the migration by doing the following in the
  " migrate" file at the folloiwng path ./bin/db/migrate 
                 
                       last_successful_run = set_last_successful_run(file_time)

- The above ensures that the last successful run is not against the current time but the last time it ran ( or was executed) and we run the command ./bin/db/setup to get the folloiwng output

 
  ![migration](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/93f4c9eb-bea5-4b39-8a15-6f2fbd8d4120)

  
- We create a new file "ActivityShowItem.js" at the path ./frontend-react-js/src/components/ActivityShowItem.js along with changes in activitiyitem.css and activitiycontent.css to further fine tune the rendering of
  our pages in the application



                                 import './ActivityItem.css';
                                 import ActivityActionReply  from '../components/ActivityActionReply';
                                 import ActivityActionRepost  from '../components/ActivityActionRepost';
                                 import ActivityActionLike  from '../components/ActivityActionLike';
                                 import ActivityActionShare  from '../components/ActivityActionShare';

                                 import { Link } from "react-router-dom";
                                 import { format_datetime, time_ago, time_future } from '../lib/DateTimeFormats';
                                 import {ReactComponent as BombIcon} from './svg/bomb.svg';

                                 export default function ActivityShowItem(props) {

                                   const attrs = {}
                                   attrs.className = 'activity_item expanded'
                                   return (
                                     <div {...attrs}>
                                       <div className="acitivty_main">
                                         <div className='activity_content_wrap'>
                                           <div className='activity_content'>
                                             <Link className='activity_avatar'to={`/@`+props.activity.handle} ></Link>
                                             <div className='activity_meta'>
                                               <div className='activity_identity' >
                                                 <Link className='display_name' to={`/@`+props.activity.handle}>{props.activity.display_name}</Link>
                                                 <Link className="handle" to={`/@`+props.activity.handle}>@{props.activity.handle}</Link>
                                               </div>{/* activity_identity */}
                                               <div className='activity_times'>
                                                 <div className="created_at" title={format_datetime(props.activity.created_at)}>
                                                   <span className='ago'>{time_ago(props.activity.created_at)}</span> 
                                                 </div>
                                                 <div className="expires_at" title={format_datetime(props.activity.expires_at)}>
                                                   <BombIcon className='icon' />
                                                   <span className='ago'>{time_future(props.activity.expires_at)}</span>
                                                 </div>
                                               </div>{/* activity_times */}
                                             </div>{/* activity_meta */}
                                           </div>{/* activity_content */}
                                           <div className="message">{props.activity.message}</div>
                                         </div>

                                         <div className='expandedMeta'>
                                           <div class="created_at">
                                             {format_datetime(props.activity.created_at)}
                                           </div>
                                         </div>
                                         <div className="activity_actions">
                                           <ActivityActionReply setReplyActivity={props.setReplyActivity} activity={props.activity} setPopped={props.setPopped} activity_uuid={props.activity.uuid} count=                                                            {props.activity.replies_count}/>
                                           <ActivityActionRepost activity_uuid={props.activity.uuid} count={props.activity.reposts_count}/>
                                           <ActivityActionLike activity_uuid={props.activity.uuid} count={props.activity.likes_count}/>
                                           <ActivityActionShare activity_uuid={props.activity.uuid} />
                                         </div>
                                       </div>
                                     </div>
                                   )
                                 }




       
  ![Homepage](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/25c88023-291b-40f7-b441-40dd7695aff3)

  
    
  ![Addingotheruser](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/cf371f67-863d-412e-ba9a-36ee426bd1db)



###  Cleanup Part 2

- We check whether the AWS RDS Production DB is upto date by checking whether the "reply_to_activity_uuid" has a type which is " integer " or " uuid". Since it was still " integer" we needed to run the migration on 
  the Prod database by running the following command.

            CONNECTION_URL=$PROD_CONNECTION_URL ./bin/db/migrate ( this is done to override the connection url to prod connection url)
 
- We check the whether the migration has run properly or not logging into the Prod database by the command ./bin/db/connect prod and get to see the following output where the type is changed to uuid, thereby making 
  it possible for us to generate replies in the application.
   
   
  ![migrate_prod](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/181871d3-f204-4255-9b64-28ee0da40a1d)
 
 
- We now want to roll out the latest changes in the backend and front end application by doing the following
- Rolling out Backend Change, we run a CICD pipeline to merge the " main" branch into "production".

 ![pushchangestordsthroughcicd](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/0bcb1281-accf-40ab-96b4-7535acbef601)


- Rolling out the frontend changes in the application is through a sync tool. 
- The bash script file in the path  ./bin/frontend/static-build is executed after correcting the errors that we encounter and post the successfull build in whichn we get the following output in the gitpod terminal

  ![static-build](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/668656ec-d45f-4a3c-a4b8-608726303471)

- We then run the sync file on the path  ./bin/frontend/sync and it is executed after correcting error by doing the change of adding changeset.json in the erb/sync.env.erb file as given below 

              SYNC_OUTPUT_CHANGESET_PATH=<%=  ENV['THEIA_WORKSPACE_ROOT'] %>/tmp/changeset.json
     
- This generates a changeset file in form of An invalidation file on the cloudfront as shared below. 

  ![Cloudfront Invalidation1](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/226efe6d-1d9c-4ff3-8609-4752a415c52d)


- We run the Production Dynamodb Database : CrdDdb-DynamoDBTable-TPSQ22XBXP1B in the local environment to check whether it runs properly or not before running it in Production environment after making changes in the
  files at the path following path where we set the environment varibles for the Production DynmoDB Database.
   
             aws/cfn/machine-user/config.toml
             aws/cfn/service/template.yaml
             backend-flask/lib/ddb.py
             erb/backend-flask.env.erb 
             
- We update the service template with the envr by running the command at the path ./bin/cfn/service which generates a cfn changeset for execution, post which we do a pull request by merging "main" into "production"
- We get a error " security token included in the request is invalid " on crudding in our application ,which is observed in the cloudwatch logs and the same is resolved by created a role " machineuser" using a CFN
  template having the permissions to read and write into the Production DynamoDB Table - CrdDdb-DynamoDBTable-TPSQ22XBXP1B
- Following CFN templates are added at the following paths. 


            config.toml at the path aws/cfn/machine-user/config.toml
            template.yaml at the path aws/cfn/machine-user/template.yaml
            machineuser at the following path bin/cfn/machineuser
            
            frontend-react-js/src/pages/MessageGroupPage.js
  
  ![machineuser](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/120da5d9-bbb0-4cca-a8cc-85d1b87ce360)

  ![machineuser_resource](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/3c738fd8-7607-4806-8237-08fb0fe84815)

 - The machine user role's access key id and secret access keys are stored in the parameter store under the following variables
      
             /cruddur/backend-flask/AWS_ACCESS_KEY_ID
             /cruddur/backend-flask/AWS_SECRET_ACCESS_KEY

 - The above details are rolled out by releasing the change in the code pipeline : CrdCicd-Pipeline-CBU5WJZASPM1. Once the pipeline execution is successfull, we do check the application by login with another user

 - Once the pipeline execution is successfull, we do check the application by login with another user ,but we cant send the message and the same is corrected by changes in the MessageGroupPage.js at the following 
   path : frontend-react-js/src/pages/MessageGroupPage.js

 - Since the changes wer made to the frontend files we run these again which generates a new invalidation file in the cloudfront distribution :  https://di38zz9ba2r5u.cloudfront.net    
 
              ./bin/frontend/static-build
              ./bin/frontend/sync
 
  ![frontend_sync](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/8550457f-365d-4455-b72a-668fb185d320)


 - The above bursts the cloudfront cache with the creation of the following invalidation file at the cloudfront

 
   ![Cloudfront Invalidations2](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/60930e92-3812-4117-ab2b-ff245d17f8e9)

         
- The final outputs that we can see on our application on sending messages to another user along with snapshot of the messages in the Production Dynamodb Database : CrdDdb-DynamoDBTable-TPSQ22XBXP1B


 ![HomePage ](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/27e6eec1-074d-49ed-90da-3696c1a8c431)

 ![Messages (2)](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/4cf543d5-1e74-4410-9bee-9b439546f4d4)
 
 
 ![messages](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/47055e53-6479-436f-a1f1-9857723aaeab)

 
 ![messagebyotheruser](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/9437d5f7-6da3-4619-acd2-5be0843745f0)
 
  
 ![notifications](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/23c3a596-45ad-443c-a851-e4da240593f4)


![DynamoDB Messages](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/d5a3943d-9adf-4316-b4ae-ce461358a53d)



  















 
