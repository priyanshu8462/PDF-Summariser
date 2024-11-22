import boto3
import requests

s3_client = boto3.client(
    's3',
    aws_access_key_id='aws_access_key_id',
    aws_secret_access_key='aws_secret_access_key'
)

#Generate the presigned URL
# response = s3_client.generate_presigned_post(
#     Bucket = 'pdf-summariser-demo',
#     Key = OBJECT_NAME_TO_UPLOAD,
#     ExpiresIn = 10 
# )

# print(response)

# #Upload file to S3 using presigned URL
# files = { 'file': open(OBJECT_NAME_TO_UPLOAD, 'rb')}
# r = requests.post(response['url'], data=response['fields'], files=files)
# print(r.status_code)


def upload_file_to_s3(file_obj, file_name, bucket_name='pdf-summariser-demo'):
    # Generate the presigned URL for direct upload
    response = s3_client.generate_presigned_post(
        Bucket=bucket_name,
        Key=file_name,
        ExpiresIn=10
    )
    
    # Upload file to S3 using presigned URL
    files = {'file': file_obj}
    upload_response = requests.post(response['url'], data=response['fields'], files=files)
    return upload_response.status_code