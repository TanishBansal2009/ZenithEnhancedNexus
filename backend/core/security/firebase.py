import os
from firebase_admin import credentials, initialize_app, storage

CRED_PATH = os.getenv("FIREBASE_CREDENTIALS", "c:/Users/tanis/Desktop/Zen/credentials.json")
BUCKET_NAME = os.getenv("FIREBASE_BUCKET", "zen-9999.appspot.com")

cred = credentials.Certificate(CRED_PATH)
firebase_app = initialize_app(cred, {"storageBucket": BUCKET_NAME})
bucket = storage.bucket(app=firebase_app)

def upload_file(local_path, remote_path):
    """Upload a file to Firebase Storage."""
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_path)
    return f"gs://{BUCKET_NAME}/{remote_path}"

def download_file(remote_path, local_path):
    """Download a file from Firebase Storage."""
    blob = bucket.blob(remote_path)
    blob.download_to_filename(local_path)
    return local_path

def list_files(prefix=""):
    """List files in the Firebase bucket under a prefix."""
    return [blob.name for blob in bucket.list_blobs(prefix=prefix)]

def delete_file(remote_path):
    """Delete a file from Firebase Storage."""
    blob = bucket.blob(remote_path)
    blob.delete()
    return True
