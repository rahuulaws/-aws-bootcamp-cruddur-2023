# Week 12 — Week X 

### Sync tool for static website hosting

 - We started off by creating a bash script file - static build. Details as below. It is executed manually by changing directory in gitpod terminal to the front-react-js path.
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
 
