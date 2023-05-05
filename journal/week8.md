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
  
  ![cdnoutput](https://user-images.githubusercontent.com/77395830/236403295-a2c5fddc-7a3e-47db-bedc-83be50720307.jpg)

  - domain_name>In order to visit https://assets.<your_domain_name>/avatars/data.jpg to see the processed image, we need to create a record via Route 53:Amazon CloudFront is designed to work seamlessly with S3 to serve your S3 content in a faster way. Also, using CloudFront to serve s3 content gives you a lot more flexibility and control. To create a CloudFront distribution, a certificate in the us-east-1 zone for *.<your_domain_name> is required. If you don't have one yet, create one via AWS Certificate Manager, and click "Create records in Route 53" after the certificate is issued.



 
ctoring of scripts and making the code user friendly was a great experience but extremely heavy one for me who has a Zero background in coding. 
 - ChatGPT and Bootcampers on Discord once again helped me to get through this week.
 - As they say, the proof of pudding is in eating and using my own domain name to access Cruddur application was a highlight for me. 
