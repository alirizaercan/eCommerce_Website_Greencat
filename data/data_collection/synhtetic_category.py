import csv
import os
from datetime import datetime
import random

# Directory and file setup
csv_dir = os.path.join('data', 'raw')
os.makedirs(csv_dir, exist_ok=True)
csv_filename = os.path.join(csv_dir, "category.csv")

# Category names
category_names = [
    "Elektronik", "Moda", "Mutfak", "KisiselBakim", "Kitap", "Spor", "Oyuncak", "Saglik", "Otomotiv", "Supermarket"
]

# Function to generate random descriptions
def generate_description(name):
    descriptions = [
        f"{name} kategorisine ait ürünler.",
        f"{name} ürünlerinde geniş seçenekler.",
        f"En iyi {name} ürünlerini burada bulabilirsiniz.",
        f"{name} için özel fırsatlar."
    ]
    return random.choice(descriptions)

# Generate current timestamp
def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create the CSV file
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(["category_id", "category_name", "category_description", "created_at", "modified_at"])
    
    # Write data
    for category_id, category_name in enumerate(category_names, start=1):
        description = generate_description(category_name)
        created_at = current_timestamp()
        modified_at = created_at
        writer.writerow([category_id, category_name, description, created_at, modified_at])

print(f"{csv_filename} oluşturuldu ve dolduruldu.")
