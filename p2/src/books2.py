from datetime import date

from .helper.api_response import ApiResponse

from .models.book import Book , RatingEnum

from fastapi import FastAPI, Path , HTTPException
from starlette import status

app = FastAPI()


Books  = [
    Book(id=1, title="The Great Gatsby", author="F. Scott Fitzgerald", category="Classic", description="A novel set in the Roaring Twenties.", rating=RatingEnum.FIVE, release_date=date(1925, 4, 10)),
    Book(id=2, title="To Kill a Mockingbird", author="Harper Lee", category="Classic", description="A novel about racial injustice in the Deep South.", rating=RatingEnum.FIVE, release_date=date(1960, 7, 11)),
    Book(id=3, title="1984", author="George Orwell", category="Dystopian", description="A novel about a totalitarian regime that uses surveillance and propaganda to control its citizens.", rating=RatingEnum.FOUR, release_date=date(1949, 6, 8)),
    Book(id=4, title="The Catcher in the Rye", author="J.D. Salinger", category="Classic", description="A novel about teenage rebellion and alienation.", rating=RatingEnum.FOUR, release_date=date(1951, 7, 16)),
    Book(id=5, title="The Lord of the Rings", author="J.R.R. Tolkien", category="Fantasy", description="An epic fantasy novel about the quest to destroy the One Ring.", rating=RatingEnum.FIVE, release_date=date(1954, 7, 29))
]

@app.get("/")
async def read_root():
    return ApiResponse(status_code=200, message="Welcome to the Books API").to_dict()

@app.get("/books")
async def get_books():
    return ApiResponse(status_code=200, message="Books retrieved successfully", data=Books).to_dict()

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.post("/books")
async def create_book(book: Book):
    Books.append(book)
    return ApiResponse(status_code=201, message="Book created successfully", data=book).to_dict()

@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(Books):
        if book.id == book_id:
            Books[index] = updated_book
            return ApiResponse(status_code=200, message="Book updated successfully", data=updated_book).to_dict()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(Books):
        if book.id == book_id:
            deleted_book = Books.pop(index)
            return ApiResponse(status_code=200, message="Book deleted successfully", data=deleted_book).to_dict()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")