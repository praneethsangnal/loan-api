from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:praneeth@localhost:5433/loan_db"

# communication with database
engine = create_engine(DATABASE_URL) 

# private session for each user
SessionLocal = sessionmaker(bind=engine)

#match python classes names with column names
Base = declarative_base()