from fastapi import FastAPI
from .routes.classifier import router as classifier_router

def create_app() -> FastAPI:
    app = FastAPI(title="Classifier API", version="1.0")
    app.include_router(classifier_router)
    return app

app = create_app()
