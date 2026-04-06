from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scheme

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/loans")
def get_loans(db: Session = Depends(get_db)):
    schemes = db.query(Scheme).limit(10).all()
    return schemes