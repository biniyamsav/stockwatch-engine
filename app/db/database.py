from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine(url=settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)