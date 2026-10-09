from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


# =====================  CATEGORIES  =====================
@app.post(
    "/categories/",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    if crud.get_category_by_name(db, category.name):
        raise HTTPException(status_code=400, detail="Category name already exists")
    return crud.create_category(db, category)


@app.get("/categories/", response_model=List[schemas.CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


# =====================  BOOKS  =====================
@app.post(
    "/books/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # 400 if category does not exist
    if not crud.get_category(db, book.category_id):
        raise HTTPException(status_code=400, detail="Category does not exist")
    # 400 if duplicate ISBN
    if crud.get_book_by_isbn(db, book.isbn):
        raise HTTPException(status_code=400, detail="ISBN already exists")
    return crud.create_book(db, book)


@app.get("/books/", response_model=List[schemas.BookResponse])
def read_books(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    # 404 if filtering by a category that does not exist
    if category_id is not None and not crud.get_category(db, category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.get_books(db, category_id)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)
):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_update.category_id is not None and not crud.get_category(
        db, book_update.category_id
    ):
        raise HTTPException(status_code=400, detail="Category does not exist")

    if book_update.isbn is not None and book_update.isbn != db_book.isbn:
        if crud.get_book_by_isbn(db, book_update.isbn):
            raise HTTPException(status_code=400, detail="ISBN already exists")

    return crud.update_book(db, db_book, book_update)


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, db_book)
    return {"message": "Book deleted successfully"}
