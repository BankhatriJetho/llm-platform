from datasets import Dataset
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
import os

MODEL_DIR = "models"

def fine_tune_model(dataset_path: str):
    """Fine-tune a pre-trained model using the given dataset."""
    try:
        print(f"Starting fine-tuning process for dataset: {dataset_path}")
        
        # Ensure model directory exists
        os.makedirs(MODEL_DIR, exist_ok=True)
        print(f"Model directory checked/created at: {MODEL_DIR}")
        
        # Load dataset
        try:
            df = pd.read_csv(dataset_path)
            texts = df["text"].tolist()
            labels = df["label"].tolist()

            # Map string labels to integers
            label_mapping = {"positive": 1, "negative": 0}
            labels = [label_mapping[label.lower()] for label in labels]
            
            print(f"Dataset loaded successfully. Number of records: {len(df)}")
        except Exception as e:
            return {"error": f"Failed to read dataset: {str(e)}"}
        
        # Load pre-trained model and tokenizer
        model_name = "distilbert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
        print(f"Pre-trained model and tokenizer loaded successfully: {model_name}")
        
        # Tokenize dataset
        try:
            encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)
            dataset = Dataset.from_dict({
                "input_ids": encodings["input_ids"],
                "attention_mask": encodings["attention_mask"],
                "labels": labels,
            })
            print(f"Dataset tokenized successfully. Sample input IDs: {encodings['input_ids'][:3]}")
        except Exception as e:
            return {"error": f"Failed to tokenize dataset: {str(e)}"}
        
        # Define Trainer and TrainingArguments
        try:
            training_args = TrainingArguments(
                output_dir=MODEL_DIR,
                num_train_epochs=3,
                per_device_train_batch_size=8,
                save_steps=10,
                save_total_limit=2,
                logging_dir=f"{MODEL_DIR}/logs",
                logging_steps=5,
            )
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=dataset,
            )
            print("Trainer and TrainingArguments defined successfully.")
        except Exception as e:
            return {"error": f"Failed to define Trainer: {str(e)}"}
        
        # Fine-tune the model
        try:
            print("Starting fine-tuning...")
            trainer.train()
            model.save_pretrained(MODEL_DIR)
            tokenizer.save_pretrained(MODEL_DIR)
            print("Fine-tuning completed successfully.")
        except Exception as e:
            return {"error": f"Fine-tuning failed: {str(e)}"}
        
        return {"message": "Fine-tuning completed successfully", "model_dir": MODEL_DIR}
    except Exception as e:
        return {"error": f"Unexpected error during fine-tuning: {str(e)}"}


