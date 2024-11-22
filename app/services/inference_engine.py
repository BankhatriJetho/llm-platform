import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_DIR = "models"

def run_inference(input_text: str):
    """
    Perform inference on the given input text using the fine-tuned model.
    """
    if not os.path.exists(MODEL_DIR):
        raise Exception("Model directory not found. Please fine-tune the model first.")
    
    # Load the fine-tuned model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    
    # Tokenize input text
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1).item()
    
    # Decode predictions into labels
    label_map = {0: "negative", 1: "positive"}
    return label_map.get(predictions, "unknown")
