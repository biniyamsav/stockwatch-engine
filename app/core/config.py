from pydantic_settings import BaseSettings

class settings(BaseSettings):
    PROJECT_NAME:str="inventory_alert_service"
    ENV:str="development"
    DEBUG:bool=True 
    API_V1_PREFIX:str="/api/v1"
    DATABASE_URL:str="name_of_database"

settings = settings()