from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ComparisonResult(Base):
    __tablename__ = "comparison_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    home_price: Mapped[float] = mapped_column(Float, nullable=False)
    monthly_rent: Mapped[float] = mapped_column(Float, nullable=False)
    mortgage_rate: Mapped[float] = mapped_column(Float, nullable=False)
    investment_return_rate: Mapped[float] = mapped_column(Float, nullable=False)
    buy_total_cost: Mapped[float] = mapped_column(Float, nullable=False)
    rent_total_cost: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
