from fastapi import FastAPI

app = FastAPI(
    title="Vision AI",
    description="Vision AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Vision AI API!"}