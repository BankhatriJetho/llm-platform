def manage_datasets():
    return "Dataset manager logic goes here"
import os
import pandas as pd

DATA_DIR = "data"

def list_datasets():
    """List all datasets in the data directory."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    return os.listdir(DATA_DIR)

def validate_and_save_dataset(file_name: str, content: bytes):
    """Validate and save the dataset."""
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, file_name)

    # Check if the file is a CSV
    if not file_name.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    # Save the file temporarily
    with open(file_path, "wb") as f:
        f.write(content)

    # Validate the dataset
    try:
        df = pd.read_csv(file_path)
        required_columns = ["text", "label"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Dataset must contain columns: {required_columns}")
    except Exception as e:
        os.remove(file_path)  # Remove invalid file
        return {"error": str(e)}

    return {"message": f"Dataset {file_name} uploaded and validated successfully", "path": file_path}
