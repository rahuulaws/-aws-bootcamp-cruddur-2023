# Week 8 — Serverless Image Processing

 - Completed the Tasks listed out for the Week. 
 - Got an opportunity to work with AWS CDK, Typescript along with other AWS services at a very detailed level to serve an image through the application. 
 - As always, ChatGPT and Bootcampers on Discord once again helped me to get through this week.
 - I am now able to appreciate the high that developers gets on seeing a deployment/feature work and then ultimately seeing the application work.


 ### Implement CDK to deploy an Serverless Image processing Solution
 
 - Used CDK to do the following
 
 -   Create a S3 Bucket cloudnoww-cruddur-uploaded-avatars for storing the original uploaded avatar images ( ex.data.jpg).
 -   Create a  Lambda fn -ThumbLambda to process the uploaded images in the S3 Bucket cloudnoww-cruddur-uploaded-avatars and stores the final processed 
     image (data.jpg) into the folder - avatars of the manually created S3 bucket - assets.cloudnoww.com from which the processed images are served in the profile page
     of cruddur app.                
        

 ![cloudnoww-cruddur-uploaded-avatars - uploads](https://user-images.githubusercontent.com/77395830/236397508-7b995012-0259-421a-a62c-99d10751072f.png)
 
 
 
 
 ![assets.cloudnoww.com - processed image](https://user-images.githubusercontent.com/77395830/236397737-ba85bbca-544c-4033-bdeb-98f0d8f74230.jpg)
 
 
 
  ### Serving Avatars via CloudFront and a sub Domain created in Route 53. 

  - A CDN - Content Delivery network like AWS Cloudfront is used to serve both static and dynamic content. In our case, the processed images are stored in the
    S3 Bucket - assets.cloudnoww.com which are mapped to the Cloudfront distribution.
  - An A- Record is created with a sub domain - assets.cloudnoww.com with Alias pointed towards CloudFront distribution
  - My profile image can be accessed through https://assets.cloudnoww.com/avatars/data.jpg
  - Invalidation feature of CDN can be configured by using the object path /avatars/* to deliver the updated avatar images uploaded by the consumer. 

 ![Cloudfrontimage](https://user-images.githubusercontent.com/77395830/236408121-8738d768-dc80-4f84-8e56-facb9e655c54.jpg)


  ### Implement Users Profile Page and Database Migrations
  
   - Relevant scripts are updated and new ones created where required in backend-flask and frontend-react-js 
   - A new column called bio will be created because the Postgres DB did not have the column for saving a brief about the user - a bio, we need to run scripts for
     migration so that user can write a brief about themselves and update as when required.
     
     
     ![Migrate](https://user-images.githubusercontent.com/77395830/236409994-6b06f8f3-1e42-49b5-b862-b3e7aa8e4da5.jpg)
     
     
   ### Implement Avatar uploading
   
   - We want to allow users of our app to update their profile image and this is achieved by generating an pre-signed url invoked through an API Gateway endpoint by
     allowing them to upload image in an S3 bucket - cloudnoww-cruddur-uploaded-avatars from where the processing image workflow kicks in to deliver the image to the
     S3 bucket -assets.cloudnoww.com.
   - Lambda functions are created along with routes in API Gateway to ensure the above happens



   ![Final1](https://user-images.githubusercontent.com/77395830/236413480-10e18aea-5c21-485e-b6e0-11aa8f028dc2.jpg)

     
