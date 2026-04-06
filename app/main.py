from fastapi import FastAPI
from app.routes.loans import router as loan_router
from app.routes.genai import router as genai_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Student Loan Navigator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(genai_router)
app.include_router(loan_router)

@app.get("/")
def home():
    return {"message": "API is running"}