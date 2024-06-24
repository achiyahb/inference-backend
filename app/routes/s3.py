import boto3
from fastapi import HTTPException
from io import BytesIO
from app.config import settings

s3_client = boto3.client('s3',
                             aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region_name
                             )

model_cache = {}

def get_model_from_s3(model_id: str):
    if model_id in model_cache:
        return model_cache[model_id]
    
    model_file_key = f"models/{model_id}.pkl"
    model_file_stream = BytesIO()
    try:
        s3_client.download_fileobj(settings.s3_bucket, model_file_key, model_file_stream)
        model_file_stream.seek(0)
        model_bytes = model_file_stream.read()
        model_cache[model_id] = model_bytes
        return model_bytes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading model: {str(e)}")