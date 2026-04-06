from fastapi import FastAPI
from app.routes.loans import router as loan_router

app = FastAPI(title="Student Loan Navigator API")

app.include_router(loan_router)

@app.get("/")
def home():
    return {"message": "API is running"}