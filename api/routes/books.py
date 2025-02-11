from typing import OrderedDict

from fastapi import APIRouter, status, HTTPException, Depends, Path
from fastapi.responses import JSONResponse

from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter()

# Initialize in-memory database with some books
db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}

# Custom path converter to validate book ID


def validate_book_id(book_id: str = Path(...)):
    if not book_id.isdigit():
        raise HTTPException(status_code=404, detail="Book not found")
    return int(book_id)

# Route to create a new book


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )

# Route to get all books


@router.get(
    "/", response_model=OrderedDict[int, Book], status_code=status.HTTP_200_OK
)
async def get_books() -> OrderedDict[int, Book]:
    return db.get_books()

# Route to update an existing book by ID


@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book: Book, book_id: int = Depends(validate_book_id)) -> Book:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=db.update_book(book_id, book).model_dump(),
    )

# Route to delete a book by ID


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Depends(validate_book_id)):
    db.delete_book(book_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

# Route to get a single book by ID


@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Depends(validate_book_id)) -> Book:
    book = db.get_book(book_id)
    if book:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=book.model_dump(),
        )
    raise HTTPException(status_code=404, detail="Book not found")
