from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables
from routes.reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application"""
    print("Starting up the application...")
    create_db_and_tables()
    print("Database and tables created successfully.")
    yield
    print("Shutting down the application...")


app = FastAPI(
    title="PVR API",
    description="Reviews api for PVR",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {"message": "Welcome to the PVR API!"}

app.include_router(reviews_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000 , reload=True)