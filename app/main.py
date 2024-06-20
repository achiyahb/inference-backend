from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.classifier import router as classifier_router

def create_app() -> FastAPI:
    app = FastAPI(title="Classifier API", version="1.0")

    origins = [
        "http://localhost",  # Front-end running on localhost
        "http://localhost:3002",  # Front-end running on a different port
        "http://127.0.0.1:3002",  # Another common localhost setup
        # Add other origins if needed
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )   

    app.include_router(classifier_router)
    return app

app = create_app()
