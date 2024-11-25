from app.services.dataset_manager import validate_dataset

# Path to the dataset file
dataset_path = "data/dataset.csv"

# Run validation
result = validate_dataset(dataset_path)
print(result)
