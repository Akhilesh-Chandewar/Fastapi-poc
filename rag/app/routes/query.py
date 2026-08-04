from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_service import rag_query

router = APIRouter(
    prefix="/query",
    tags=["query"],
    responses={404: {"description": "Not found"}},
)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class Source(BaseModel):
    page: int | None = None
    text: str


class QueryResponse(BaseModel):
    query: str
    response: str
    sources: list[Source]


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        result = rag_query(request.query, k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query failed: {e}")

    return QueryResponse(**result)
