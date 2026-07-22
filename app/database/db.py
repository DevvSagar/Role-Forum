from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from app.config import get_app_config

config = get_app_config()

engine = create_engine(config.database_url)
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
        raise