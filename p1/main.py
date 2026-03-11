import os
import uvicorn

from .src.books import app

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run(app=app, host=HOST, port=PORT, log_level="info")
