# S3 Uploader

- [S3 Uploader](#s3-uploader)
  - [Package](#package)
  - [Deploy](#deploy)
  - [Query Outputs](#query-outputs)

The S3 Uploader creates a static web site hosted on S3 which allows to upload jpeg images to an S3 bucket using presigned urls.

## Package

```sh
# Set a stack name
STACK_NAME=uploader-$(openssl rand -hex 4)

# Create a custom bucket
CUSTOM_BUCKET=uploader-$(openssl rand -hex 4)-s3uploadpackage-$(openssl rand -hex 6)
aws s3 mb s3://${CUSTOM_BUCKET}

# Package
aws cloudformation package --s3-bucket ${CUSTOM_BUCKET} --template-file ./s3-uploader.cfn.yaml --output-template-file ./s3-uploader-packaged.cfn.yaml
```

## Deploy

```sh
aws cloudformation deploy --stack-name ${STACK_NAME} --template-file ./s3-uploader-packaged.cfn.yaml --capabilities CAPABILITY_IAM
```

## Query Outputs

```sh
# Get outputs
API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} | jq -r --arg stack ${STACK_NAME} '.Stacks[] | select(.StackName==$stack) | .Outputs[] | select(.OutputKey=="APIendpoint") | .OutputValue')

FRONTEND_BUCKET=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} | jq -r --arg stack ${STACK_NAME} '.Stacks[] | select(.StackName==$stack) | .Outputs[] | select(.OutputKey=="S3UploadFrontendBucketName") | .OutputValue')

WEBSITE_URL=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} | jq -r --arg stack ${STACK_NAME} '.Stacks[] | select(.StackName==$stack) | .Outputs[] | select(.OutputKey=="WebsiteURL") | .OutputValue')

# Print url
echo Website: ${WEBSITE_URL}
```
