from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, INTEGER

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("id", INTEGER, primary_key=True),
    Column("genre_id", ForeignKey("genres.id")),
    Column("movie_id", ForeignKey("movies.id")),
)

class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)

class Movie(Base):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    director: Mapped[str] = mapped_column(db.String(100), nullable=False)
    year: Mapped[int] = mapped_column(db.Integer, nullable=False)
    genre: Mapped[Genre] = relationship(secondary=movie_genres)
