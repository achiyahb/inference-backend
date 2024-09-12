from fastai.vision.all import load_learner, PILImage
from io import BytesIO
from torch import device, load

class ClassifierModel:
    def __init__(self, model_stream: BytesIO):
        self.model = self.load_model_from_stream(model_stream)

    @staticmethod
    def load_model_from_stream(model_stream: BytesIO):
      
        model_stream.seek(0)
        return load(model_stream, map_location=device('cpu'))

    def predict(self, image_path: str) -> str:
        image = PILImage.create(image_path)
        prediction = self.model.predict(image)
        return prediction[0]



