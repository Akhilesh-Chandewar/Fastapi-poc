from fastapi import FastAPI , Request
import uvicorn

app = FastAPI(
    title="FastAPI Foundation",
    description="FastAPI Foundation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
async def read_root(request: Request):
    """Root endpoint that returns a welcome message and status and helth check information."""
    return {
        "Message": "Welcome to FastAPI Foundation!",
        "Status": "Success",
    }

@app.get("/about")
async def about():
    """About endpoint that returns information about the API Metadata."""
    return {
        "Service": "FastAPI Foundation",
        "Version": "1.0.0",
        "Team": "FastAPI Foundation Team",
        "Region": "Global",

    }

@app.get("/orders")
async def orders():
    """Orders endpoint that returns a list of orders."""
    return [
        {"id": 1, "name": "Order 1"},
        {"id": 2, "name": "Order 2"},
        {"id": 3, "name": "Order 3"},
        {"id": 4, "name": "Order 4"},
        {"id": 5, "name": "Order 5"},
    ]

@app.get("/orders/status")
async def order_status():
    """Get order status."""
    return {
        "orders": [
            {"id": 1, "status": "Pending"},
            {"id": 2, "status": "Shipped"},
            {"id": 3, "status": "Delivered"},
            {"id": 4, "status": "Cancelled"},
            {"id": 5, "status": "Returned"},
        ]
    }


if __name__ == "__main__":
    uvicorn.run("01_fastapi_foundation:app", host="0.0.0.0", port=8000, reload=True)