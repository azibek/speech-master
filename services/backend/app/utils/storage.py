# GCS helpers
import mimetypes, pathlib

from google.cloud import storage
from google.oauth2.credentials import Credentials
import json

# Load previously saved credentials
with open("token.json", "r") as token_file:
    token_info = json.load(token_file)
    print("#"*30, "\n", token_info)
    creds = Credentials.from_authorized_user_info(token_info)

# Pass credentials explicitly to the client
client = storage.Client(credentials=creds)




# client = storage.Client()
bucket = client.bucket("speak-like-idol-assets")

def upload_file(local_path: str, blob_name: str):
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    blob.content_type = mimetypes.guess_type(local_path)[0]
    return generate_signed_url(blob)

def upload_bytes(data: bytes, blob_name: str, content_type: str):
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data, content_type=content_type)
    return generate_signed_url(blob)

def generate_signed_url(blob, minutes=60):
    return blob.generate_signed_url(expiration=minutes*60)
