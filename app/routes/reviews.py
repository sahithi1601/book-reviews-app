from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all reviews
@router.get("/reviews/", response_model=List[schemas.Review])
def read_reviews(db: Session = Depends(get_db)):
    return db.query(models.Review).all()

@router.post("/reviews/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_review = models.Review(book_id=review.book_id, rating=review.rating, comment=review.comment)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.put("/reviews/{review_id}", response_model=schemas.Review)
def update_review(review_id: int, updated_review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.book_id = updated_review.book_id
    review.content = updated_review.content
    review.rating = updated_review.rating
    db.commit()
    db.refresh(review)
    return review

@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return {"detail": "Review deleted successfully"}
