# GCS helpers
from google.cloud import storage
import mimetypes, pathlib

client = storage.Client()
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
