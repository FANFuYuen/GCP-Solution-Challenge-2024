import boto3

def UploadToS3(file_name,bucket_name,folder_name):
    # Create a client object for S3 service
    s3_client = boto3.client('s3')

    # Specify the key name for the photo
    key_name = folder_name + '/' + file_name

    # Specify the local file name and path for the photo
    local_file_name = file_name
    local_file_path = 'C:\\A05\\FYP-test\\webcam_photo\\'+local_file_name

    
    # Upload the photo to S3 bucket using the client object
    s3_client.upload_file(local_file_path, bucket_name, key_name,ExtraArgs={'ACL':'public-read', 'ContentType': 'image/jpeg', 'ContentDisposition': 'inline'})
    
    # Print a success message
    print('Photo uploaded successfully to S3 bucket.')


def main():
    file_name = 'cam_12023-10-18-20-53-59.jpg'
    folder_name = 'boss-email'
    bucket_name = '220073549'
    UploadToS3(file_name,bucket_name,folder_name)

if __name__ == "__main__":
    main()
