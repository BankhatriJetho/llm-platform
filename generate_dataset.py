import pandas as pd

# Generate synthetic dataset
data = {
    "text": [
        "I love this product!",
        "This is the worst experience I've had.",
        "The service was great and timely.",
        "The app crashes often.",
        "Amazing quality and highly recommended!",
        "Not worth the money.",
    ] * 50,  # Duplicate these lines 50 times to create 300 entries
    "label": [
        "positive",
        "negative",
        "positive",
        "negative",
        "positive",
        "negative",
    ] * 50,
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to a CSV file in the 'data/' directory
output_path = "data/dataset.csv"
df.to_csv(output_path, index=False)
print(f"Synthetic dataset generated and saved to {output_path}")
