import uuid
from sqlalchemy import String, Boolean, ForeignKey, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.infrastructure.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False,  default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    sale_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class RecipeDetail(Base):
    __tablename__ = "recipe_detail"

    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), primary_key=True)
    supply_id: Mapped[str] = mapped_column(ForeignKey("supplies.id"), primary_key=True)
    supply: Mapped["Supply"] = relationship()
    amount_supply: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_measure: Mapped[str] = mapped_column(String(10), nullable=False)


