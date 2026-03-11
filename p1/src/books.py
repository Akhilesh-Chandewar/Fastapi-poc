from .helper.api_response import ApiResponse
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "category": "Fiction",
    },
    {"id": 2, "title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {
        "id": 3,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category": "Fiction",
    },
    {
        "id": 4,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "category": "Romance",
    },
    {
        "id": 5,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "category": "Fiction",
    },
    {
        "id": 6,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "category": "Fantasy",
    },
    {
        "id": 7,
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "category": "Fantasy",
    },
    {"id": 8, "title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy"},
    {
        "id": 9,
        "title": "Dune",
        "author": "Frank Herbert",
        "category": "Science Fiction",
    },
    {
        "id": 10,
        "title": "Neuromancer",
        "author": "William Gibson",
        "category": "Science Fiction",
    },
]


@app.get("/")
def read_root():
    res = ApiResponse(status_code=200, message="Welcome to the Book API!")
    return res.to_dict()


@app.get("/books")
def get_books():
    res = ApiResponse(status_code=200, data=books)
    return res.to_dict()


@app.get("/books/search")
def search_books(
    author: Optional[str] = None,
    category: Optional[str] = None,
    title: Optional[str] = None,
):
    filtered_books = books
    if author:
        filtered_books = [
            b for b in filtered_books if author.lower() in b["author"].lower()
        ]
    if category:
        filtered_books = [
            b for b in filtered_books if category.lower() in b["category"].lower()
        ]
    if title:
        filtered_books = [
            b for b in filtered_books if title.lower() in b["title"].lower()
        ]
    res = ApiResponse(status_code=200, data=filtered_books)
    return res.to_dict()


@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        res = ApiResponse(status_code=200, data=book)
    else:
        res = ApiResponse(status_code=404, message="Book not found")
    return res.to_dict()


@app.post("/books")
def add_book(book: dict):
    new_id = max(b["id"] for b in books) + 1
    book["id"] = new_id
    books.append(book)
    res = ApiResponse(status_code=201, message="Book added successfully", data=book)
    return res.to_dict()

@app.put("/books/{book_id}")
def update_book(book_id: int, book: dict):
    existing_book = next((b for b in books if b["id"] == book_id), None)
    if existing_book:
        existing_book.update(book)
        res = ApiResponse(status_code=200, message="Book updated successfully", data=existing_book)
    else:
        res = ApiResponse(status_code=404, message="Book not found")
    return res.to_dict()

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    global books
    books = [book for book in books if book["id"] != book_id]
    res = ApiResponse(status_code=200, message="Book deleted successfully")
    return res.to_dict()

