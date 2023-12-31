import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.infrastructure.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    sale_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    register_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    details = relationship("RecipeDetail", cascade="all, delete-orphan", back_populates="product")

class RecipeDetail(Base):
    __tablename__ = "recipe_detail"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    supply_id: Mapped[str] = mapped_column(ForeignKey("supplies.id"))
    supply: Mapped["Supply"] = relationship()
    amount_supply: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    product = relationship("Product", back_populates="details")