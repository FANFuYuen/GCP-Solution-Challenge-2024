# FYP-A05
Hi, all test FYP in there!






# Example of Uploading File to Cloud Storage
https://stackoverflow.com/questions/37003862/how-to-upload-a-file-to-google-cloud-storage-on-python-3

from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os


credentials_dict = {
    'type': 'service_account',
    'client_id': os.environ['BACKUP_CLIENT_ID'],
    'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
    'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
    'private_key': os.environ['BACKUP_PRIVATE_KEY'],
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)
client = storage.Client(credentials=credentials, project='myproject')
bucket = client.get_bucket('mybucket')
blob = bucket.blob('myfile')
blob.upload_from_filename('myfile')


# if git push need user name/pas 

git config --global user.name "John Doe"
git config --global user.email johndoe@example.com


# if want git clone github branch

git clone -b branch_name repository_url

# download all puin
pip install -r requirements.txt 



pip install -r requirements.txt