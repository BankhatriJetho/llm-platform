from fastapi import APIRouter, HTTPException, Body
from app.services.inference_engine import run_inference

router = APIRouter()

@router.post("/inference", tags=["inference"])
async def inference_endpoint(input_text: str = Body(..., embed=True)):
    """
    Make a prediction using the fine-tuned model.
    """
    if not input_text:
        raise HTTPException(status_code=400, detail="Input text is required")
    try:
        prediction = run_inference(input_text)
        return {"input_text": input_text, "prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
