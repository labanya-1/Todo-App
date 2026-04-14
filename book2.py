from http.client import HTTPException
from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(gt=0, lt=6)
    published_date : int = Field( gt= 1999 , lt= 2030)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Labanya Roy",
                "description": "a description of new book",
                "rating": "5",
                "published_date":"2005"
            }
        }
    }


BOOKS = [
    Book(1, "Atomic Habits", "James Clear", "Build good habits and break bad ones", 4.8, 2000),
    Book(2, "The Alchemist", "Paulo Coelho", "A journey of dreams and destiny", 4.5, 2005),
    Book(3, "Rich Dad Poor Dad", "Robert Kiyosaki", "Financial education and mindset", 4.4, 2007),
    Book(4, "Deep Work", "Cal Newport", "Focus and productivity in a distracted world", 4.6, 2009),
    Book(5, "Ikigai", "Hector Garcia", "Finding purpose and happiness in life", 4.3, 2020)
]


@app.get("/")
async def root():
    return {"message": "Welcome to Book API", "docs": "/docs"}


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/rating/{book_rating}",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: float = Path(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/books/publish", status_code=status.HTTP_200_OK)
async def publish_date(published_date:int = Query(gt= 1999 , lt= 2030)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create_books",status_code=status.HTTP_201_CREATED)
async def create_books(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed= False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed= True
    if not book_changed:
        raise HTTPException(status_code=404,detail="item not found")


@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail="item not found")