from typing import Optional
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

def get_filtered_loans(
    db,
    marks10=None,
    marks12=None,
    state=None,
    caste=None,
    gender=None,
    limit=10
):
    query = db.query(Scheme)

    # 🟢 HARD FILTERS
    if marks10 is not None:
        query = query.filter(Scheme.min_10th_marks <= marks10)

    if marks12 is not None:
        query = query.filter(Scheme.min_12th_marks <= marks12)

    if state is not None:
        query = query.filter(
            (Scheme.eligible_states == "ALL") |
            (Scheme.eligible_states.ilike(f"%{state}%"))
        )

    if caste is not None:
        query = query.filter(
            (Scheme.eligible_castes == "ALL") |
            (Scheme.eligible_castes.ilike(f"%{caste}%"))
        )

    if gender is not None:
        query = query.filter(
            (Scheme.eligible_genders == "ALL") |
            (Scheme.eligible_genders.ilike(f"%{gender}%"))
        )

    schemes = query.all()

    # 🟡 SOFT FILTERS / SCORING
    result = []

    for s in schemes:
        score = 0

        if s.interest_rate_min:
            score += (100 - s.interest_rate_min)

        if s.maximum_amount:
            score += (s.maximum_amount / 100000)

        if s.loan_processing_fee is not None:
            score += (10 - s.loan_processing_fee)

        result.append({
            "scheme_name": s.scheme_name,

            # ranking
            "interest_rate": s.interest_rate_min,
            "max_amount": s.maximum_amount,
            "processing_fee": s.loan_processing_fee,
            "score": round(score, 2),

            # display
            "repayment_period": s.repayment_period,
            "moratorium_period": s.moratorium_period,
            "parent_criteria": s.parent1_profession_criteria,
            "achievement_required": s.govt_achievements_required
        })

    result.sort(key=lambda x: x["score"], reverse=True)

    return result[:limit]


@router.get("/loans/filter")
def filter_loans(
    marks10: Optional[float] = None,
    marks12: Optional[float] = None,
    state: Optional[str] = None,
    caste: Optional[str] = None,
    gender: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_filtered_loans(
        db,
        marks10=marks10,
        marks12=marks12,
        state=state,
        caste=caste,
        gender=gender,
        limit=limit
    )

@router.get("/loans/{loan_id}")
def get_loan_detail(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Scheme).filter(Scheme.id == loan_id).first()

    if not loan:
        return {"error": "Loan not found"}

    return {
        "scheme_name": loan.scheme_name,

        # financial
        "interest_rate_min": loan.interest_rate_min,
        "interest_rate_max": loan.interest_rate_max,
        "maximum_amount": loan.maximum_amount,
        "processing_fee": loan.loan_processing_fee,
        "prepayment_charges": loan.prepayment_charges,

        # eligibility
        "min_10th_marks": loan.min_10th_marks,
        "min_12th_marks": loan.min_12th_marks,
        "eligible_states": loan.eligible_states,
        "eligible_castes": loan.eligible_castes,
        "eligible_genders": loan.eligible_genders,

        # advanced
        "parent1_criteria": loan.parent1_profession_criteria,
        "parent2_criteria": loan.parent2_profession_criteria,
        "govt_achievements": loan.govt_achievements_required,

        # loan terms
        "repayment_period": loan.repayment_period,
        "moratorium_period": loan.moratorium_period
    }