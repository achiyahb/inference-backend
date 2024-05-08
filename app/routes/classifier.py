from fastapi import APIRouter, HTTPException, UploadFile, File
import shutil
import os
from ..models import classifier_model
from ..schemas import PredictionResponse

router = APIRouter()

@router.post("/classify", response_model=PredictionResponse)
async def classify(file: UploadFile = File(...)) -> PredictionResponse:
    try:
        # Ensure the file is an image
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File provided is not an image.")

        # Save the uploaded image temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Predict using the path to the temporary file
        prediction = classifier_model.predict(temp_file_path)
        
        # Remove the temporary file
        os.remove(temp_file_path)

        return PredictionResponse(prediction=prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
