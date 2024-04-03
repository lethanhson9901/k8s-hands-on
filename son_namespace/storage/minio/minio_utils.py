from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv
# Add this import at the top of your script
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Load environment variables from .env file
load_dotenv()
# print(os.getenv('MINIO_SERVER'))

def list_bucket_objects(bucket_name):
    # Create a client with the MinIO server hostname, and access and secret keys.
    minio_client = Minio(
        os.getenv('MINIO_SERVER'),  # Replace with your MinIO server's address and port
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False  # Set to True if using https, False otherwise
    )

    # List objects in the specified bucket
    try:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        print(objects)
        for obj in objects:
            print(obj)
    except S3Error as err:
        # Print out the error response for debugging
        print("S3 Error:", err)
        if err.response is not None:
            print("Response data:", err.response.data.decode())
        else:
            print("No response data.")
    except Exception as exc:
        print("An unexpected error occurred:", exc)

# Usage
list_bucket_objects("influxdb-backup")
