from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.config.env import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Import all models here to ensure they are associated with Base


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
