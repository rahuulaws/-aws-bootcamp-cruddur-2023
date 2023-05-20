## Architecture Guide

Before you run any templates, be sure to create an S3 bucket to contain
all of our artifacts for CloudFormation.

```
aws s3 mk s3://cfn-artifacts-cloud-bootcamp
export CFN_BUCKET="cfn-artifacts-cloud-bootcamp"
gp env CFN_BUCKET="cfn-artifacts-cloud-bootcamp"
```

> remember bucket names are unique to the provided code example you may need to adjust