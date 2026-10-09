from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------- Category ----------
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Book ----------
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=1, max_length=20)
    publication_year: Optional[int] = Field(None, ge=0, le=2100)
    stock_quantity: int = Field(1, ge=0)
    category_id: int


class BookUpdate(BaseModel):
    """All fields optional so PUT can update only what is sent."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=1, max_length=20)
    publication_year: Optional[int] = Field(None, ge=0, le=2100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: Optional[int] = None
    stock_quantity: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)
