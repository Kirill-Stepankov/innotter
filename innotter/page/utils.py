import boto3
from django.conf import settings

session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

s3 = session.client("s3", endpoint_url=settings.AWS_ENDPOINT_URL)


def upload_file_s3(file, key):
    s3.put_object(
        Body=file,
        Bucket=settings.BUCKET_NAME,
        Key=key,
    )
