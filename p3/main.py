import os
import uvicorn

from src.todo import TodoApp

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))



if __name__ == "__main__":
    todo_app = TodoApp()
    uvicorn.run(todo_app.app, host=HOST, port=PORT)
