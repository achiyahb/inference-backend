from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region_name: str
    port: int = Field(default=8001, env='APP_PORT')
    host: str = Field(default="0.0.0.0", env='APP_HOST')
    inference_front_url: str = Field(..., env='INFERENCE_FRONTEND_URL')
    s3_bucket: str = Field(..., env='S3_BUCKET')
    trainer_node_service_url: str = Field(..., env='TRAINER_NODE_SERVICE_URL')
    jwt_token: str = Field(..., env='JWT_TOKEN')

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
