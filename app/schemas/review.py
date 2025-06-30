from pydantic import BaseModel

class ReviewCreate(BaseModel):
    book_id: int
    rating: int
    comment: str

class Review(ReviewCreate):
    id: int

    class Config:
        from_attributes = True
