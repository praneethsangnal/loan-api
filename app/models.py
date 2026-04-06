from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base

class Scheme(Base):
    __tablename__ = "government_schemes"

    id = Column(Integer, primary_key=True, index=True)

    # Basic info
    scheme_name = Column(String)

    # Financial details
    interest_rate_min = Column(Float)
    interest_rate_max = Column(Float)
    maximum_amount = Column(Float)
    loan_processing_fee = Column(Float)
    prepayment_charges = Column(Float)

    # Academic eligibility
    min_10th_marks = Column(Float)
    min_12th_marks = Column(Float)

    # Eligibility filters
    eligible_states = Column(String)
    eligible_castes = Column(String)
    eligible_genders = Column(String)

    # Advanced eligibility (important for real logic)
    parent1_profession_criteria = Column(Text)
    parent2_profession_criteria = Column(Text)
    govt_achievements_required = Column(Text)

    # Loan terms (useful for comparison)
    repayment_period = Column(String)
    moratorium_period = Column(String)