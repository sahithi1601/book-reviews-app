from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import books, reviews

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)
app.include_router(reviews.router)
