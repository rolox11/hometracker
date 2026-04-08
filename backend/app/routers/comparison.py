from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ComparisonResult

router = APIRouter(prefix="/api/comparison", tags=["comparison"])

LOAN_TERM_YEARS = 30
DOWN_PAYMENT_PCT = 0.20


class ComparisonInput(BaseModel):
    home_price: float = Field(gt=0)
    monthly_rent: float = Field(gt=0)
    mortgage_rate: float = Field(gt=0, description="Annual rate as a percentage, e.g. 6.5")
    investment_return_rate: float = Field(gt=0, description="Annual rate as a percentage, e.g. 7.0")


class ComparisonOutput(BaseModel):
    home_price: float
    monthly_rent: float
    mortgage_rate: float
    investment_return_rate: float
    monthly_mortgage_payment: float
    buy_total_cost: float
    rent_total_cost: float
    recommendation: str


def _monthly_mortgage(principal: float, annual_rate_pct: float, years: int) -> float:
    r = (annual_rate_pct / 100) / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def _compute(inp: ComparisonInput) -> dict:
    down_payment = inp.home_price * DOWN_PAYMENT_PCT
    loan = inp.home_price - down_payment
    monthly_payment = _monthly_mortgage(loan, inp.mortgage_rate, LOAN_TERM_YEARS)
    months = LOAN_TERM_YEARS * 12

    # Opportunity cost: the down payment invested instead
    monthly_investment_return = (inp.investment_return_rate / 100) / 12
    opportunity_cost = down_payment * (
        (1 + monthly_investment_return) ** months - 1
    )

    buy_total_cost = (monthly_payment * months) + down_payment + opportunity_cost
    rent_total_cost = inp.monthly_rent * months

    return {
        "home_price": inp.home_price,
        "monthly_rent": inp.monthly_rent,
        "mortgage_rate": inp.mortgage_rate,
        "investment_return_rate": inp.investment_return_rate,
        "monthly_mortgage_payment": round(monthly_payment, 2),
        "buy_total_cost": round(buy_total_cost, 2),
        "rent_total_cost": round(rent_total_cost, 2),
        "recommendation": "buy" if buy_total_cost < rent_total_cost else "rent",
    }


@router.post("", response_model=ComparisonOutput)
def create_comparison(inp: ComparisonInput, db: Session = Depends(get_db)):
    result = _compute(inp)
    record = ComparisonResult(
        home_price=inp.home_price,
        monthly_rent=inp.monthly_rent,
        mortgage_rate=inp.mortgage_rate,
        investment_return_rate=inp.investment_return_rate,
        buy_total_cost=result["buy_total_cost"],
        rent_total_cost=result["rent_total_cost"],
    )
    db.add(record)
    db.commit()
    return result


@router.get("", response_model=list[ComparisonOutput])
def list_comparisons(db: Session = Depends(get_db)):
    rows = db.query(ComparisonResult).order_by(ComparisonResult.created_at.desc()).limit(50).all()
    return [
        {
            "home_price": r.home_price,
            "monthly_rent": r.monthly_rent,
            "mortgage_rate": r.mortgage_rate,
            "investment_return_rate": r.investment_return_rate,
            "monthly_mortgage_payment": round(
                _monthly_mortgage(
                    r.home_price * (1 - DOWN_PAYMENT_PCT),
                    r.mortgage_rate,
                    LOAN_TERM_YEARS,
                ),
                2,
            ),
            "buy_total_cost": r.buy_total_cost,
            "rent_total_cost": r.rent_total_cost,
            "recommendation": "buy" if r.buy_total_cost < r.rent_total_cost else "rent",
        }
        for r in rows
    ]
