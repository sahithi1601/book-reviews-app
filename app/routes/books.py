from typing import List  
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books/", response_model=List[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    # Add average rating to each book
    for book in books:
        if book.reviews:
            book.average_rating = sum(review.rating for review in book.reviews) / len(book.reviews)
        else:
            book.average_rating = None
    return books

@router.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated_book: schemas.BookCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = updated_book.title
    book.author = updated_book.author
    db.commit()
    db.refresh(book)
    return book

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}
