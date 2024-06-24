import boto3
from app.config import settings


s3_client = boto3.client('s3',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region_name
)

def download_file(model_file_key, model_file_stream):
    print(f"Downloading model file from S3: {model_file_key}")

    s3_client.download_fileobj(settings.s3_bucket, model_file_key, model_file_stream)