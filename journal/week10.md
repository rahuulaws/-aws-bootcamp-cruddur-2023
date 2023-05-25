# Week 10 and Week 11 — CloudFormation

 - Completed the Tasks listed out for the CFN Week. 
 - It was a fabulous opportunity to work handson with CFN for deploying multiple AWS services. I could not have asked for more.
 - This was the the only week, where I did not need to take support from my fellow Bootcampers and ChatGPT at a very minimal level.

 ### Context and Background 
 
  - The objective of this week is to use the Infrastructure as a Code (IaC) Service : AWS Cloudformation Tool to create AWS Infrastructure and deploy the Cruddur application on it.
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
 - Config.toml file which has key configuration details such as the name of the stack, region of deployment, S3 Bucketname details are referenced by the CFN template.
 - Bash script kept under the path ./bin/cfn/networking is run which deploys the CFN template with aws cli command.
  
 ![network](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/dd37e40e-0cf9-482c-bbf0-13f8389c6d67)
 
 ![NetworkResource](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/91b6bbf8-1325-4cb2-96f1-b12fb69111a9)

 ![networkconsole](https://github.com/rahuulaws/-aws-bootcamp-cruddur-2023/assets/77395830/cc815589-019c-41eb-a7bf-251eca40b32e)
    
   
