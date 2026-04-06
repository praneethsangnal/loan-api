from fastapi import FastAPI
from app.routes.loans import router as loan_router
from app.routes.genai import router as genai_router


app = FastAPI(title="Student Loan Navigator API")
app.include_router(genai_router)
app.include_router(loan_router)

@app.get("/")
def home():
    return {"message": "API is running"}