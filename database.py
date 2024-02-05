from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

DATABASE_URI = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URI)
sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    database = sessionLocal()
    try:
        yield database
    finally:
        database.close()
