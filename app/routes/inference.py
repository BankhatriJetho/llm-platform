from fastapi import APIRouter

router = APIRouter()

@router.post("/inference")
def run_inference():
    return {"message": "Inference endpoint placeholder"}
