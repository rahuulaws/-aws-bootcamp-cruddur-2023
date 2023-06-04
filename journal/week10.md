# Week 10 and Week 11 — CloudFormation

 - Completed the Tasks listed out for the CFN Week. 
 - It was a fabulous opportunity to work handson with CFN for deploying multiple AWS services. I could not have asked for more.
 - This was the the only week, where I did not need to take support from my fellow Bootcampers and ChatGPT at a very minimal level.


### Context and Background 
 
  - The objective of this Two week is to use the Infrastructure as a Code (IaC) Service : AWS Cloudformation Tool to create AWS Infrastructure and deploy the Cruddur application on it.
  - Cloudformation helps us to define the desired cloud environment using code writen in either Yaml or Json, known as templates, instead of manually configuring each resource.
  - The key benefits for using AWS Cloudformation can be listed  as below : https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html
    - Simplify infrastructure management
    - Quickly replicate your infrastructure
    - Easily control and track changes to your infrastructure
   - Do note we have used YAML script to write the AWS Cloudformation templates
   - Each AWS Service/Infrastructure was created and deployed by creating a folder structure in the AWS trre in our Gitpod environment.
   - As an representation I am showing the snapshot of the template for the ECS Cluster creation, detail steps such as folder creation in Gitpod which stores the template in yaml and in another folder
     a Bash Script for AWS CLI to initiate the deployment of AWS Cloudformation of template,which would not be done for other services that we deploy using CFN.

 
 ### Create a ECS Cluster using Cloudformation template - Completed in the first episode with the AWS Guest.
 
   - We started off by creating a folder named cfn under AWS in our Gitpod environment with a template.yaml stored in it. 
   - This Cloudformation template as below would create the ECS Cluster
   
   ![ECSTemplate](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/35bb5168-5393-46d1-abe7-c286f6b4715c)
   
   - A bash script is used to to deploy the the cloudformation template with aws cli command and the same is stored in the path ./bin/cfn/deploy and the final copy of the template stored 
     in an S3 bucket : cfn-artifacts-cloud-bootcamp
    
   ![ECSBashScript](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/686c04a5-af1d-4e60-9759-6f4d7d041f32)
   
   - We are expected to review the changset in the AWS Cloudformation console which will depict the changes that have been applied to the resources before the changeset is executed.
   - AWS Cloudformation Console details as below 
    
   ![CFNConsole_mycluster](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/88ce0e75-5eee-49c5-953a-30ec3a0ab3f8)

       
   ![mycluster](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/c30c37c3-17ba-44ad-9cef-187b173e92e4)
   
   
   ![ecscluster](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/c5d4d99f-d27b-49d2-887a-0e57f01f60be)
   
   
 
 ### Network Layer using Cloudformation template
 
 - We started off by creating a Networking folder under cfn with the path aws/cfn/networking
 - Created CFN template and put in the above path to deploy VPC, IGW, AttachIGW, RouteTable, RouteToIGW, public and private Subnets, SubnetRTAssociation and outputs.
 - Config.toml file which has key configuration details such as the name of the stack - CrdNet, region of deployment, S3 Bucketname details are referenced by the CFN template.
 - Bash script kept under the path ./bin/cfn/networking is run which deploys the CFN template with aws cli command.
   
 ![network](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/dd37e40e-0cf9-482c-bbf0-13f8389c6d67)
 
 ![NetworkResource](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/91b6bbf8-1325-4cb2-96f1-b12fb69111a9)

 ![networkconsole](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/cc815589-019c-41eb-a7bf-251eca40b32e)
  
 ![Output](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/85659130-399a-4a4e-af2a-c8001348428a)
 
 ![Parameter](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/c1dcc32d-9256-4601-b09f-4105b22fc610)


 
 ### CFN Diagramming the Network Layer
 
 https://lucid.app/lucidchart/c7d244d1-6828-476c-bf84-018094ccfcff/edit?viewport_loc=-1388%2C-438%2C3292%2C1626%2C0_0&invitationId=inv_55d53435-b0d8-40d4-b543-13a818781a36
 
 ![Network Layer](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/9fdf774f-9cee-44b9-8e2f-7dd46fdb4aca)

 
  ### Cluster Layer using Cloudformation template
  
 - We started off by creating a Cluster folder under cfn with the path aws/cfn/cluster
 - Created CFN template and put in the above path to deploy the following 
     -  ECS Fargate Cluster
     - Application Load Balanacer (ALB)
        - ipv4 only
        - internet facing
        - certificate attached from Amazon Certification Manager (ACM)
    - ALB Security Group
    - HTTPS Listerner
       - send naked domain to frontend Target Group
       - send api. subdomain to backend Target Group
    - HTTP Listerner
       - redirects to HTTPS Listerner
    - Backend Target Group
    - Frontend Target Group
  
 - Config.toml file which has key configuration details such as the name of the stack -CrdCluster , region of deployment, S3 Bucketname, Certificate ARN are referenced by the CFN template.
 - Bash script kept under the path ./bin/cfn/cluster is run which deploys the CFN template with aws cli command.
 - Kindly note, I did not delete the ALB /TG which were created earlier along with the  ECS cluster's task frontend-react-js and backend whcih were created in week 6
 - Delete the ALB and target group which we created already.

![cluster](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/f8fbc6e3-4abc-4b53-b433-a497efcb045b)
 
![Output](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/92b8ef68-7848-4dcf-99cd-8ba75177983a)

![Parameter](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/1df8ceda-f927-42c6-acbc-99f8bc4af2c8)

![FargateCluster](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/1a3da62d-c790-4999-9d0a-45e70f4a7918)

![clusteralb](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/4bc5fdb2-eda1-4545-ada1-ec9fad755731)

![ALBTG](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/f4512909-dda1-4db1-a86d-c8840a12f335)

![FrontendTG](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/bd94be2f-a6ef-491b-bc41-400b33f9d315)

![BckendTG](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/10ff4ea9-ac00-4f8c-bb9a-85edb051fef0)


### CFN Diagramming the Cluster Layer

https://lucid.app/lucidchart/7e4c3054-c659-4295-a5f6-591b00345cbf/edit?viewport_loc=-2875%2C-484%2C5178%2C2439%2C0_0&invitationId=inv_d7a3157d-25ce-473c-97d2-fbc80b13dcd0

![Cluster-1](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/54d488db-9a4e-4472-84d4-d2ea3d707e1f)

![Cluster-2](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/19af9fe9-e26f-40f8-bec9-7375e8252adb)


### Service Layer using Cloudformation template

 - We started off by creating a Service folder under cfn with the path aws/cfn/service
 - Created CFN template and put in the above path to deploy the following
   - Task Definition
   - Fargate Service
   - Execution Role
   - Task Role
 
 - Config.toml file which has key configuration details such as the name of the stack -CrdSrvBackendFlask , region of deployment, S3 Bucketname, Envr Variables for Frontend and Backend URls,DDB MessageTble are
   referenced by the CFN template.
 - Bash script kept under the path ./bin/cfn/service is run which deploys the CFN template with aws cli command.
 
 ![CFNFargateCluster1](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/6f4dd995-ca54-4938-abab-065b8ac5342b)
 
 ![Reources](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/9e664d61-e663-4275-8351-d4db9a6d17ec)

![Outputs](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/e1be2a4e-3b05-402e-b65c-a88a6a7e892d)

![fargate-service-console](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/6102402a-1426-4361-8f05-7c8c40b82253)

![Backendflask](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/f15a3bbb-b7e2-41db-8fdc-64f33f989bee)

![BackendHealthCheck](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/481160a2-af5d-4ba1-83c7-2d3be81a9bbc)


### AWS RDS using Cloudformation template

 - We started off by creating a DB folder under cfn with the path aws/cfn/db
 - Created CFN template and put in the above path to deploy the following
   - The primary Postgres RDS Database for the application
     - RDS Instance
     - Database Security Group
     - DBSubnetGroup
  - Config.toml file which has key configuration details such as the name of the stack -CrdDb, region of deployment, S3 Bucketname amd parameters such as the name of Neworking and Clsuter stack along with the
   MasterUsername for RDS are referenced by the CFN template.
 - set the env var for MasterUserPassword of RDS in gitpod
 - Bash script kept under the path ./bin/cfn/db is run which deploys the CFN template with aws cli command.

![CFN_RDS](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/a0416bf0-c2ce-44da-b369-2d6e7a1a7050)

![CFN_Resource](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/ba92c355-ca52-4c08-b2f9-ec9b14212525)

![RDS Created](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/52a364ad-7d3f-4cd7-82ac-43f7f49e814f)

![RDS Console](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/ce7d7cdf-832d-4473-bb6e-f48283e6cda6)


- The Endpoint url of the Postgres is changed in the parameter store with the RDS RB created through CFN

![ParameterStore](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/74b8b22f-6d75-408e-a291-866326f479ed)


### CFN - Diagramming Service and RDS

https://lucid.app/lucidchart/b1487e50-594a-49a9-ba1d-abdad40d9ebb/edit?viewport_loc=-3712%2C-3152%2C6904%2C3252%2C0_0&invitationId=inv_f74d0e01-f680-443a-bca3-106f1d02aa35


![Service and RDS](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/ba77cb6a-156f-424a-8388-a431f1ba5b7a)



### AWS Lambda, Dynamodb and DynamoDB Streams using Serverless Application Module(SAM) Cloudformation template

 - We started off by creating a DDB folder under cfn with the path aws/cfn/ddb
 - Created CFN template and put in the above path to deploy the following
   - The primary Postgres RDS Database for the application
     - DynamoDB Table
     - DynamoDB Stream
     - LambdaLogGroup
     - ExecutionRole for lambda
 - SAM is installed in Gitpod and Gitpod.yml
 - AWS Serverless Application Model - Build serverless applications in simple and clean syntax : https://aws.amazon.com/serverless/sam/
    - The AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings.
    - With just a few lines per resource, one can define the application they want and model it using YAML.
    - During deployment, SAM transforms and expands the SAM syntax into AWS CloudFormation syntax, enabling one to build serverless applications faster.
    - Use the AWS SAM CLI or AWS Cloud Development Kit (CDK) to start building SAM-based applications.
    - One can also use the SAM CLI to deploy applications to AWS, or create secure CI/CD pipelines that follow best practices and integrate with AWS.
 - Bash script is created for SAM Build, SAM PACKAGE and SAM DEPLOY
 - create a bash script file to sam build, sam package and sam deploy
 
 ![SAM Scripts](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/a75ac822-8d4d-404e-b398-a076d43c0c64)
 
 - Run the bash script - ./ddb/build ; ./ddb/package and ./ddb/deploy to get the following outputs.

![CFN_DDB_Console](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/801dfc27-f86a-4b2c-9f57-d341a89647ff)


![CFN_Resources](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/d42abe6b-3262-45f9-b5d1-97ea381fbaba)


![CFN_Parameters](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/0703857b-fc40-43fd-bb1a-d0345e34e896)


![ddb-console](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/93d97f43-6095-4a80-bced-e792e88b235e)


![DDB Stream](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/0a5c1c9b-8c00-414c-a525-80553500dea1)


![lambda-dynamodbstream](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/5741a060-dcdd-4901-a82b-dd484d9f2fa3)


### CFN - Diagramming DynamoDB

https://lucid.app/lucidchart/88412ee8-8044-4edf-bdd5-0beab842e225/edit?viewport_loc=-3492%2C-3220%2C6904%2C3252%2C0_0&invitationId=inv_21128b34-d4eb-465e-aa66-736a32c96021


![Dynamo DB](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/19feb9fb-69bd-45b7-94e3-f67c273566dc)



### AWS CICD Pipeline using Cloudformation template

 - We started off by creating a cicd folder under cfn with the path aws/cfn/cicd
 - Created CFN template and put in the above path to deploy the following
      - CodeStar Connection V2 Github
      - CodePipeline
      - Codebuild
     
  - Config.toml file which has key configuration details such as the name of the stack -CrdCicd, region of deployment, S3 Bucketname amd parameters such as 
       - ServiceStack = 'CrdSrvBackendFlask'
       - ClusterStack = 'CrdCluster'
       - GitHubBranch = 'production'
       - GithubRepo = 'rahuulaws/-aws-bootcamp-cruddur-2023'
       - ArtifactBucketName = "codepipeline-cruddur-artifacts-cfn"
       - BuildSpec = 'backend-flask/buildspec.yml
    
  - We created a Nested CFN stack to create Codebuild Project through codebuild.yaml
      - Codebuild used for baking container images
      - Codebuild Project
      - Codebuild Project Roled in gitpod
      
 - Bash script kept under the path ./bin/cfn/cicd is run which deploys the CFN template with aws cli command.
 - New S3 bucket is created manually through AWS console with the name - codepipeline-cruddur-artifacts-cfn to store the artifacts. 
 
 ![S3Bucket](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/f9c342ce-1af4-46c5-a8b8-04e957b75cfc)
 
 
![cicd-cfn](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/eaec762b-0026-450c-8e12-1b558d7867a1)


![cicd-resource](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/3dced92e-a9e6-435d-b1d4-21b684dc2069)


![NestedCICD 225526](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/76d26813-66ed-459e-85e0-0c420b1583c9)

 
![NestedCICD Outputs](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/f80bc7bf-b4bc-4678-80a7-c4293f321eaa)


![NestedCICD Parameters](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/9519c698-e3d9-4d26-8fc7-5a7156150a31)


![NestedCICD Resources](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/ebf461ee-d4fc-4936-99aa-fdf7612d65d0)


![CICD Console](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/4bd2cb09-94dc-4e65-8f58-06b0df1e76f7)


![Codepipeline Visualization](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/9901ab32-a32e-494d-9243-50a8f977f0c5)


### CFN Diagramming CICD

https://lucid.app/lucidchart/488fdf65-bdde-4562-82d9-8d332ca15e56/edit?viewport_loc=-5731%2C-2494%2C10788%2C5081%2C0_0&invitationId=inv_d4f5f12a-3465-4a93-8ab6-b247363aaa7e


![CIcd-1](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/1dba0335-e8d8-4dcc-9a5e-6463e55235b0)


![CICD-2](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/bfea52b4-7512-445f-b0fa-53b449a6d8ce)


### Static Website Hosting Frontend using Cloudformation template

 - We started off by creating a frontend folder under cfn with the path aws/cfn/frontend
 - Created CFN template and put in the above path to deploy the following
     - CloudFront Distribution
     - S3 Bucket for www.
     - S3 Bucket for naked domain
     - RootBucketDomain
     - WwwBucketDomain
     - Bucket Policy
 
 - Config.toml file which has key configuration details such as the name of the stack -CrdFrontend , region of deployment, S3 Bucketname and the following parameters are set 
     - CertificateArn = 'arn:aws:acm:us-east-1:881652387149:certificate/aa888fb5-12b2-41c4-b9d9-7bb9a3fd292d'
     - WwwBucketName = 'www.cloudnoww.com'
     - RootBucketName = 'cloudnoww.com'  
     - Remove the Type A record from the Route53 for the rootdomainname.
    - Bash script kept under the path ./bin/cfn/frontend is run which deploys the CFN template with aws cli command.
     
     
  ![CFNFrontendDetails](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/2dcaf817-e144-454c-bf60-4e4801fc2ede)


  ![CFNFrontendResources](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/865293cf-a695-4a64-89f9-8df510c3124f)


  ![CFNFrontendParameters](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/1312b640-f35d-47a2-99b7-8ed6848e76dc)


  ![CloudfrontCFN](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/22ae7157-eb44-4fb0-803a-68b276285c51)


  ![CloudfrontCFNDetails](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/ee83e50f-15ab-4987-9adb-66323521d552)


  ![Route53CFN](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/dc2feed0-f27c-401d-a8d1-c5e602d63eb4)


  ![S3Bucket](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/81402373-035e-4c9b-884a-130713be74fc)


### CFN Diagramming Static Frontend

https://lucid.app/lucidchart/dc8b4908-b5e1-48c0-aaef-e08c783a4adf/edit?viewport_loc=-5419%2C-4494%2C10788%2C5081%2C0_0&invitationId=inv_8ffada55-3619-4df9-998e-29ea4065c539


![Static Frontend](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/45bfc525-6e47-47e0-9e86-7962e2d4c7a2)



