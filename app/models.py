from fastai.vision.all import load_learner, PILImage

class ClassifierModel:
    def __init__(self, model_path):
        self.model = load_learner(model_path)

    def predict(self, image_path) -> str:
        image = PILImage.create(image_path)
        prediction = self.model.predict(image)
        return prediction[0]

model_path = "model/export.pkl"
classifier_model = ClassifierModel(model_path)
