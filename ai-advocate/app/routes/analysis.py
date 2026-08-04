from fastapi import APIRouter , HTTPException
from app.config import GOOGLE_API_KEY

from app.database import contracts_collection , analysis_collection

from app.service.gemini_analysis import analyze_contract

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
    responses={404: {"description": "Not found"}},
)

@router.post("/analysis/{contract_id}")
async def get_analysis(contract_id: str):
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=404, detail="Google API key not found.")
    if not contract_id:
        raise HTTPException(status_code=404, detail="Contract ID not found.")

    contract = contracts_collection.find_one({"contract_id": contract_id})

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found.")

    contracts_collection.update_one(
        {"contract_id": contract_id},
        {"$set": {"status": "in_progress"}},
    )

    response = await analyze_contract(contract_id, contract["text_content"])

    contracts_collection.update_one(
        {"contract_id": contract_id},
        {"$set": {"status": "complete"}},
    )

    analysis_collection.update_one(
        {"contract_id": contract_id},
        {"$set": response},
        upsert=True,
    )

    return {
        "contract_id": contract_id,
        "clause_analysis": response["clause_analysis"],
        "risk_analysis": response["risk_analysis"],
        "summary": response["summary"],
    }