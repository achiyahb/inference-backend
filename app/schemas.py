from pydantic import BaseModel

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: str

class CarPredictionResponse(BaseModel):
    prediction: str
    direction: str
