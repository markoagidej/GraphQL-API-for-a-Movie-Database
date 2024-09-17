from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class BakeryProduct(Base):
    __tablename__ = 'bakery_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    category: Mapped[str] = mapped_column(db.String(100), nullable=False)