import csv
import os
from datetime import datetime

# Create the synthetic_discount function
def generate_discount_data(file_path):
    # Define the discount data
    discounts = [
        {
            "discount_id": 1,
            "discount_name": "Yılbaşı",
            "discount_description": "Yılbaşına özel %20 indirim!",
            "discount_percentage": 20.00,
            "active": True,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "modified_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            "discount_id": 2,
            "discount_name": "Bahar Fırsatı",
            "discount_description": "Bahar sezonuna özel %15 indirim!",
            "discount_percentage": 15.00,
            "active": True,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "modified_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            "discount_id": 3,
            "discount_name": "Kara Cuma",
            "discount_description": "Kara Cuma kampanyası ile %30 indirim!",
            "discount_percentage": 30.00,
            "active": True,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "modified_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            "discount_id": 4,
            "discount_name": "Anneler Günü",
            "discount_description": "Anneler Günü'ne özel %25 indirim!",
            "discount_percentage": 25.00,
            "active": True,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "modified_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            "discount_id": 5,
            "discount_name": "Sezon Sonu",
            "discount_description": "Sezon sonu indirimi ile %10 indirim!",
            "discount_percentage": 10.00,
            "active": True,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "modified_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the discount data to a CSV file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["discount_id", "discount_name", "discount_description", "discount_percentage", "active", "created_at", "modified_at"])
        for discount in discounts:
            writer.writerow([
                discount["discount_id"],
                discount["discount_name"],
                discount["discount_description"],
                discount["discount_percentage"],
                discount["active"],
                discount["created_at"],
                discount["modified_at"]
            ])

# Define the file path
file_path = "data/raw/discount.csv"

# Generate the discount data
generate_discount_data(file_path)

print(f"Discount data has been successfully written to {file_path}.")
