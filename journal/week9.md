# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

 - Completed the Tasks listed out for the Week. 
 - Got an opportunity to work with AWS CDK, Typescript along with other AWS services at a very detailed level to serve an image through the application. 
 - This was the first week, where support from ChatGPT and Bootcampers on Discord was not required for me to go through the week.

 
 ### Context and Background work
 
 - The objective of this week is Automation, wherein changes in the repository codes kickstart the process of building the image, pushing it into ECR and deploying it into the environment by using CICD pipeline, 
   thereby avoiding manual intervention.
 - New Branch is created called as production, which gives the input to AWS CodeBuild and CodePipeline in the subequennt stages. 
  
 
 ### AWS CodeBuild, AWS Codepipeline and Deploying the Pipeline 
 
  - Build a project in AWS CodeBuild : cruddur-backend-flask-bake-image
  - Create a pipeline in AWS Pipeline : cruddur-backend-fargate
  - Test the pipeline through backend-flask/app.py return health_check function by editing it to return {"success": True, "ver": 1}, 200
  - Pipeline will be initiated ( impacting the backend-flask deployment in ECS and the backend-flask TG in the ALB : where the infrastructure changes can be seen) once the changes in the code - backend-flask/app.py 
    are merged in the production branch
    
    
    
    ![Codepipeline](https://user-images.githubusercontent.com/77395830/237032672-c01ad8d9-d230-452d-a32f-d545debe98ea.jpg)


