import pandas as pd

# Define the path to your dataset
dataset_path = "data/dataset.csv"

try:
    # Load the dataset
    df = pd.read_csv(dataset_path)
    print("Dataset loaded successfully.")
    print("First 5 rows of the dataset:")
    print(df.head())
    print("\nColumns in the dataset:")
    print(df.columns)
    print("\nNumber of records in the dataset:")
    print(len(df))
    
    # Check for text and label columns
    if "text" in df.columns and "label" in df.columns:
        print("\n'text' and 'label' columns found.")
        print("\nSample 'text' and 'label':")
        print(df[["text", "label"]].head())
    else:
        print("\nError: 'text' and/or 'label' columns not found in the dataset.")
except Exception as e:
    print(f"Error loading dataset: {str(e)}")
