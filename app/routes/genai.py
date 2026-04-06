import os
import json
from fastapi import APIRouter
from groq import Groq
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scheme
from app.routes.loans import get_filtered_loans
from fastapi import Depends


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


load_dotenv()
router = APIRouter()

# Initialize Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@router.get("/genai")
def genai_query(query: str, db: Session = Depends(get_db)):
    try:
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Extract marks (as number), state, caste, gender from: '{query}'. Return ONLY JSON.",
                }
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"}
        )

        data = json.loads(chat_completion.choices[0].message.content)

        marks = data.get("marks")
        state = data.get("state")
        caste = data.get("caste")
        gender = data.get("gender")

        #  USE EXISTING LOGIC
        results = get_filtered_loans(
            db,
            marks12=marks,
            state=state,
            caste=caste,
            gender=gender
        )

        return {
            "extracted": data,
            "results": results
        }

    except Exception as e:
        return {"error": str(e)}