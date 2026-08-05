from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/analyse",
    tags=["Analyse"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def analyse_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")


    