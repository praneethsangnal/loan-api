from fastapi import APIRouter
from typing import Optional

router = APIRouter()

loans_data = [
    {"name": "Loan A", "interest": 8.5, "state": "TN", "caste": "OBC", "min_marks": 70},
    {"name": "Loan B", "interest": 7.2, "state": "TN", "caste": "General", "min_marks": 80},
    {"name": "Loan C", "interest": 6.9, "state": "KA", "caste": "OBC", "min_marks": 75}
]

@router.get("/loans")
def get_loans():
    return loans_data




@router.get("/loans/filter")
def filter_loans(
    marks: Optional[int] = None,
    state: Optional[str] = None,
    caste: Optional[str] = None
):
    result = []

    for loan in loans_data:
        if marks is not None and marks < loan["min_marks"]:
            continue

        if state is not None and loan["state"] != state:
            continue

        if caste is not None and loan["caste"] != caste:
            continue

        result.append(loan)

    return result