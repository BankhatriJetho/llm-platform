from fastapi import APIRouter, File, UploadFile, Body
from app.services import dataset_manager, fine_tuning, inference_engine
from app.logger import logger  # Import the logger
import os

router = APIRouter()

# Health check
@router.get("/health", tags=["default"])
def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "OK"}

# Dataset routes
@router.get("/datasets", tags=["datasets"])
async def list_datasets():
    logger.info("Listing datasets.")
    datasets = dataset_manager.list_datasets()
    return {"datasets": datasets}

@router.post("/datasets", tags=["datasets"])
async def upload_dataset(file: UploadFile = File(...)):
    logger.info(f"Uploading dataset: {file.filename}")
    result = dataset_manager.validate_and_save_dataset(file.filename, file.file.read())
    return result

# Fine-tuning routes
@router.post("/fine_tune", tags=["fine-tuning"])
async def fine_tune_model(dataset_name: str = Body(..., embed=True)):
    logger.info(f"Fine-tuning started for dataset: {dataset_name}")
    dataset_path = f"data/{dataset_name}"
    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found: {dataset_name}")
        return {"error": f"Dataset {dataset_name} not found"}
    result = fine_tuning.fine_tune_model(dataset_path)
    return result

# Inference routes
@router.post("/inference", tags=["inference"])
async def run_inference(input_text: str = Body(..., embed=True)):
    logger.info(f"Inference requested for input: {input_text}")
    result = inference_engine.run_inference(input_text)
    return result

# Delete dataset
@router.delete("/datasets", tags=["datasets"])
async def delete_dataset(file_name: str):
    logger.info(f"Deleting dataset: {file_name}")
    result = dataset_manager.delete_dataset(file_name)
    return result
