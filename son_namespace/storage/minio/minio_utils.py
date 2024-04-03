from minio import Minio
from minio.error import S3Error
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def list_bucket_objects(credentials, bucket_name):
    try:
        minio_client = Minio(
            credentials['url'],
            access_key=credentials['accessKey'],
            secret_key=credentials['secretKey'],
            secure=True if credentials.get('api', '') == 's3v4' else False
        )

        objects = minio_client.list_objects(bucket_name, recursive=True)
        print(objects)
        for obj in objects:
            print(obj.object_name)
    except S3Error as err:
        print("S3 Error:", err)
        if err.response is not None:
            print("Response data:", err.response.data.decode())
        else:
            print("No response data.")
    except Exception as exc:
        print("An unexpected error occurred:", exc)

# Usage
credentials = {
    "url": "http://localhost:8008",
    "accessKey": "EyIJNZRqH9elhBkJEDEx",
    "secretKey": "uz29ihZiS75mBilsV2syks1NojKoG3mVsBkaEH9C",
    "api": "s3v4",
    "path": "auto"
}

bucket_name = "influxdb-backup"
list_bucket_objects(credentials, bucket_name)
