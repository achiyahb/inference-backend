from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import shutil
import os
from ..models import ClassifierModel
from ..schemas import PredictionResponse
from app.routes.s3 import get_model_from_s3
from io import BytesIO

router = APIRouter()

@router.post("/classify", response_model=PredictionResponse)
async def classify(file: UploadFile = File(...), modelId: int = Form(...)) -> PredictionResponse:
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File provided is not an image.")

        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)

        model_bytes = get_model_from_s3(modelId)
        classifier_model = ClassifierModel(model_bytes)

        prediction = classifier_model.predict(temp_file_path)

        os.remove(temp_file_path)

        return PredictionResponse(prediction=prediction)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
