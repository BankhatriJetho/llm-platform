import os
import pandas as pd
import random
from nltk.corpus import wordnet

DATA_DIR = "data"

def manage_datasets():
    return "Dataset manager logic goes here"

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

def delete_dataset(file_name: str):
    """Delete a dataset by its file name."""
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"Dataset {file_name} deleted successfully"}
    return {"error": f"Dataset {file_name} not found"}

def validate_dataset(file_path: str):
    """
    Validates the dataset for required fields and balanced labels.
    """
    try:
        df = pd.read_csv(file_path)
        # Check for required columns
        if "text" not in df.columns or "label" not in df.columns:
            return {"error": "Dataset must have 'text' and 'label' columns."}
        
        # Check for missing values
        if df.isnull().any().any():
            return {"error": "Dataset contains missing values. Please clean the dataset."}
        
        # Check for valid labels
        valid_labels = {"positive", "negative"}
        unique_labels = set(df["label"].unique())
        if not unique_labels.issubset(valid_labels):
            return {"error": f"Invalid labels found: {unique_labels - valid_labels}"}
        
        # Check for label balance
        label_counts = df["label"].value_counts()
        imbalance_threshold = 0.2  # Adjust threshold as needed
        if abs(label_counts["positive"] - label_counts["negative"]) / len(df) > imbalance_threshold:
            return {"warning": "Dataset is imbalanced. Consider augmenting to balance it."}
        
        return {"message": "Dataset is valid", "label_counts": label_counts.to_dict()}
    except Exception as e:
        return {"error": f"Validation failed: {str(e)}"}

def augment_text(text: str, num_augmentations: int = 1):
    """
    Augments the given text by replacing words with their synonyms.
    """
    words = text.split()
    augmented_texts = []
    
    for _ in range(num_augmentations):
        new_words = words.copy()
        for i, word in enumerate(words):
            synonyms = wordnet.synsets(word)
            if synonyms:
                synonym = random.choice(synonyms).lemmas()[0].name()
                if synonym.lower() != word.lower():
                    new_words[i] = synonym
        augmented_texts.append(" ".join(new_words))
    
    return augmented_texts

def augment_dataset(file_path: str, output_path: str):
    """
    Augments the dataset to balance the labels.
    """
    df = pd.read_csv(file_path)
    augmented_rows = []
    for _, row in df.iterrows():
        if row["label"] == "negative":  # Balance negatives
            augmented_texts = augment_text(row["text"], num_augmentations=2)
            for text in augmented_texts:
                augmented_rows.append({"text": text, "label": row["label"]})
    augmented_df = pd.DataFrame(augmented_rows)
    df = pd.concat([df, augmented_df], ignore_index=True)
    df.to_csv(output_path, index=False)
    print(f"Augmented dataset saved to {output_path}")
