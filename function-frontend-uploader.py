from crhelper import CfnResource
import boto3
import fileinput

helper = CfnResource()

@helper.create
def create_site(event, _):
    # Create static web site on S3
    # Inline replacement of API endpoint

    body = ""
    with fileinput.FileInput(event['ResourceProperties']['IndexDocument']) as file:
        for line in file:
            body += line.replace("APIENDPOINT", event['ResourceProperties']['ApiEndpoint'])

    client = boto3.client("s3")

    client.put_object(
        Body=body,
        Bucket=event['ResourceProperties']['SiteBucket'],
        Key='index.html',
        ACL='public-read',
        ContentType='text/html'
    )

    body = ""
    with fileinput.FileInput(event['ResourceProperties']['ErrorDocument']) as file:
        for line in file:
            body += line

    client.put_object(
        Body=body,
        Bucket=event['ResourceProperties']['SiteBucket'],
        Key='error.html',
        ACL='public-read',
        ContentType='text/html'
    )

    # logger.info("Finished creating index.html")
    helper.Data['Result'] = "site created"

@helper.update
def sum_2_numbers(event, _):
    pass

@helper.delete
def no_op(_, __):
    pass

def handler(event, context):
    helper(event, context)