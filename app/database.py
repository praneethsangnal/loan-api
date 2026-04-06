from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# communication with database
engine = create_engine(DATABASE_URL) 

# private session for each user
SessionLocal = sessionmaker(bind=engine)

#match python classes names with column names
Base = declarative_base()