from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import shutil
import os
from ..models import ClassifierModel
from ..schemas import PredictionResponse, CarPredictionResponse
from app.utils.client import fetch_model_data
from app.routes.storage import get_model_from_cache_or_storage
from io import BytesIO
import base64
from pydantic import BaseModel

router = APIRouter()

@router.post("/classify", response_model=PredictionResponse)
async def classify(file: UploadFile = File(...), modelKey: str = Form(...), trainerId: int = Form(...)) -> PredictionResponse:
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File provided is not an image.")

        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)

        model_bytes = get_model_from_cache_or_storage(modelKey, trainerId)
        classifier_model = ClassifierModel(model_bytes)

        prediction = classifier_model.predict(temp_file_path)

        os.remove(temp_file_path)

        return PredictionResponse(prediction=prediction)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class CarPredictionRequest(BaseModel):
    image_base64: str
    hmacHex: str

@router.post('/classify/car', response_model=CarPredictionResponse)
async def classify_car(request: CarPredictionRequest) -> CarPredictionResponse:
    try:
        image_data = base64.b64decode(request.image_base64)
        
        temp_file_path = "temp_image.png"
        with open(temp_file_path, "wb") as image_file:
            image_file.write(image_data)
        
        modelData = await fetch_model_data(request.hmacHex)
        
        model_bytes = get_model_from_cache_or_storage(modelData.get('modelKey'), modelData.get('trainerId'))
        classifier_model = ClassifierModel(model_bytes)

        prediction = classifier_model.predict(temp_file_path)

        right_direction_category = modelData.get('rightDirectionCategory')
        print(f"Prediction: {prediction}, Right Direction Category: {right_direction_category}")

        direction = "left"
        if prediction.strip().lower() == right_direction_category.strip().lower():
            direction = "right"

        os.remove(temp_file_path)

        return CarPredictionResponse(prediction=prediction, direction=direction)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
