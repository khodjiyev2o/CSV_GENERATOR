from django.conf import settings
import boto3

def upload_to_s3(filepath: str, filename: str) -> bool:
    # Connect to S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )

        # Upload the file to S3
        try: 
            s3.upload_file(filepath,settings.AWS_STORAGE_BUCKET_NAME, "media/"+filename)
            return True
        except Exception:
            return Exception
        