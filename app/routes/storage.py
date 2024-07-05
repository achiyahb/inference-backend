from fastapi import HTTPException
from io import BytesIO
from ..utils.s3 import download_file

model_cache = {}

def get_model_from_cache_or_storage(model_key: str, trainer_id: int):
    if model_key in model_cache:
        return model_cache[model_key]
    
    model_file_key = f"models/{trainer_id}/{model_key}.pkl"
    model_file_stream = BytesIO()
    try:
        download_file(model_file_key, model_file_stream)
        model_file_stream.seek(0)
        model_cache[model_key] = model_file_stream
        return model_file_stream
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading model: {str(e)}")
