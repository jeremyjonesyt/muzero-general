from fastapi import APIRouter
from app.schemas.nba_data import NbaGameData

router = APIRouter()

@router.post("/predict")
async def predict_nba(data: NbaGameData):
    # This is where your basketball inference logic will go
    return {"sport": "NBA", "status": "Ready for inference"}