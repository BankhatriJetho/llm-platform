from fastapi import APIRouter, File, UploadFile, Body
from app.services import dataset_manager, fine_tuning, inference_engine
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
    """
    Upload and validate a dataset.
    """
    # Save the uploaded file temporarily
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Validate the dataset
    validation_result = dataset_manager.validate_dataset(file_path)

    if "error" in validation_result:
        # If validation fails, delete the uploaded file and return the error
        os.remove(file_path)
        return {"error": validation_result["error"]}

    # Save and confirm upload success
    return {
        "message": f"File '{file.filename}' uploaded and validated successfully.",
        "validation": validation_result,
    }


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

# Dataset delete routes
@router.delete("/datasets", tags=["datasets"])
async def delete_dataset(file_name: str):
    result = dataset_manager.delete_dataset(file_name)
    return result
