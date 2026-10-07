from fastapi import FastAPI
from app.core.config import settings 
from app.api.routes.routes import routes


app=FastAPI(title=settings.PROJECT_NAME)
app.include_router(routes)