from email.mime import message
import uuid

from fastapi import APIRouter, HTTPException, File, UploadFile
from app.config import ALLOWED_FILE_EXTENSIONS, UPLOAD_DIR
import os

from app.database import contracts_collection
from app.service.document_parser import extract_text

from app.models import Contract, ContractUploadResponse

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload", response_model=ContractUploadResponse, status_code=201)
async def upload_contract(
    file: UploadFile = File(...)
):
    """
    Endpoint to upload a contract file.
    """
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type {ext} is not allowed.")

    content = await file.read()

    size_mb = len(content) / (1024 * 1024)
    if size_mb > 10:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}{ext}"

    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(content)

    parsed_text = extract_text(file_path)

    contract = Contract(
        contract_id=uuid.uuid4().hex,
        file_name=unique_name,
        original_file_name=file.filename,
        text_content=parsed_text,
        page_count=parsed_text.count('\f') + 1,  # Assuming form feed
        word_count=len(parsed_text.split()),
    )

    contracts_collection.insert_one(contract.model_dump())

    return {
        "message": "Contract uploaded successfully.",
        "contract": contract.model_dump(),
        "id": contract.contract_id
    }


@router.get("/", response_model=list[Contract])
async def get_contracts():
    contracts = [
        Contract(**{k: v for k, v in doc.items() if k != "_id"})
        for doc in contracts_collection.find()
    ]
    return contracts

@router.get("/{contract_id}")
async def get_contract(contract_id: str):
    contract = contracts_collection.find_one({"contract_id": contract_id})
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found.")
    return Contract(**{k: v for k, v in contract.items() if k != "_id"})