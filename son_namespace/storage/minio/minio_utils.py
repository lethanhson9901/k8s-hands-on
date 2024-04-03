from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def list_bucket_objects(bucket_name):
    # Create a client with the MinIO server hostname, and access and secret keys.
    minio_client = Minio(
        os.getenv('MINIO_SERVER'), # Replace with your MinIO server's address and port
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False # Set to True if using https, False otherwise
    )

    # List objects in the specified bucket
    try:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        for obj in objects:
            print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
                  obj.etag, obj.size, obj.content_type)
    except S3Error as err:
        print("S3 Error:", err)

# Usage
list_bucket_objects("influxdb-backup")
