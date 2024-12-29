import csv
import os
from datetime import datetime
import random

# Inventory generation parameters
inventory_count = 1000  # Number of inventory records
output_directory = "data/raw"
output_file = os.path.join(output_directory, "inventory.csv")

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Generate inventory data
def generate_inventory_data():
    inventory_data = []
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for inventory_id in range(1, inventory_count + 1):
        quantity = random.randint(0, 500)  # Random quantity between 0 and 500
        inventory_data.append([
            inventory_id,
            quantity,
            current_time,
            current_time
        ])
    
    return inventory_data

# Write inventory data to CSV
def write_inventory_csv(file_path, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(["inventory_id", "quantity", "created_at", "modified_at"])
        # Write data
        writer.writerows(data)

if __name__ == "__main__":
    inventory_data = generate_inventory_data()
    write_inventory_csv(output_file, inventory_data)
    print(f"Inventory data successfully written to {output_file}")
