from fastapi import APIRouter, File, UploadFile
from app.services import dataset_manager, fine_tuning, inference_engine
from fastapi import Body
import os

router = APIRouter()

# Health check
@router.get("/health", tags=["default"])
def health_check():
    return {"status": "OK"}

# Dataset routes
@router.get("/datasets", tags=["datasets"])
async def list_datasets():
    datasets = dataset_manager.list_datasets()
    return {"datasets": datasets}


@router.post("/datasets", tags=["datasets"])
async def upload_dataset(file: UploadFile = File(...)):
    result = dataset_manager.validate_and_save_dataset(file.filename, file.file.read())
    return result



# Fine-tuning routes
@router.post("/fine_tune", tags=["fine-tuning"])
async def fine_tune_model(dataset_name: str = Body(..., embed=True)):
    dataset_path = f"data/{dataset_name}"
    if not os.path.exists(dataset_path):
        return {"error": f"Dataset {dataset_name} not found"}
    result = fine_tuning.fine_tune_model(dataset_path)
    return result


# Inference routes
@router.post("/inference", tags=["inference"])
async def run_inference(input_text: str = Body(..., embed=True)):
    return inference_engine.run_inference(input_text)

#delete routes
@router.delete("/datasets", tags=["datasets"])
async def delete_dataset(file_name: str):
    result = dataset_manager.delete_dataset(file_name)
    return result
