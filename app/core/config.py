from pydantic_settings import BaseSettings,SettingsConfigDict

class settings(BaseSettings):
    PROJECT_NAME:str="inventory_alert_service"
    ENV:str="development"
    DEBUG:bool=True 
    API_V1_PREFIX:str="/api/v1"
    DATABASE_URL:str

    model_config = SettingsConfigDict(env_file=".env")

settings = settings()