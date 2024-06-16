from typing import List
from decouple import config
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("SECRET_KEY", cast=str)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
    ]
    PROJECT_NAME: str = "MonitorBot"
    
    class Config:
        case_sensitive = True

settings = Settings()
