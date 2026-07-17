from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)
Session_local = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()