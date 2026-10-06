from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.automl_service import AutoMLService

router = APIRouter(prefix="/api/v1/automl", tags=["AutoML Training"])

class TrainRequest(BaseModel):
    filename: str
    target_column: str

@router.post("/train")
async def run_automl_training(request: TrainRequest):
    result = await AutoMLService.train_model(request.filename, request.target_column)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result