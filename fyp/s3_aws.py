# Import boto3 library for interacting with AWS services
import os
import boto3
from webcam import current_time

# Create a client object for S3 service
s3_client = boto3.client('s3')

# Specify the bucket name and the key name for the photo
bucket_name = '220073549'
key_name = 'cam116_00_51.785653.jpg'

# Specify the local file name and path for the photo
local_file_name = key_name
local_file_path = os.path.join(os.path.dirname(__file__), '..', 'photo', 'cam116_00_51.785653.jpg')

# Upload the photo to S3 bucket using the client object
s3_client.upload_file(local_file_path, bucket_name, key_name)

# Print a success message
print('Photo uploaded successfully to S3 bucket.')