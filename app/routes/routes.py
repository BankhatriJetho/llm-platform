from fastapi import APIRouter, File, UploadFile
from app.services import dataset_manager, fine_tuning, inference_engine
from fastapi import Body

router = APIRouter()

# Health check
@router.get("/health", tags=["default"])
def health_check():
    return {"status": "OK"}

# Dataset routes
@router.get("/datasets", tags=["datasets"])
def get_datasets():
    return {"datasets": dataset_manager.list_datasets()}

@router.post("/datasets", tags=["datasets"])
async def upload_dataset(file: UploadFile = File(...)):
    if file:
        print(f"Filename: {file.filename}")
        print(f"Content Type: {file.content_type}")
        print(f"Headers: {file.headers}")
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "headers": file.headers
        }
    print("No file received.")
    return {"error": "No file received"}




# Fine-tuning routes
@router.post("/fine_tune", tags=["fine-tuning"])
async def fine_tune_model(dataset_name: str = Body(..., embed=True)):
    return {"message": fine_tuning.fine_tune_model(dataset_name)}

# Inference routes
@router.post("/inference", tags=["inference"])
async def run_inference(input_text: str = Body(..., embed=True)):
    return inference_engine.run_inference(input_text)
