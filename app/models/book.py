from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base  # ✅ This line is important

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)

    reviews = relationship("Review", back_populates="book", cascade="all, delete")
