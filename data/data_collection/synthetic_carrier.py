import csv
import os
import random

def generate_phone():
    """Generate a random Turkish phone number."""
    return f"+90{random.randint(500, 599)}{random.randint(1000000, 9999999)}"

def generate_email(carrier_name):
    """Generate a synthetic email for the carrier."""
    domain = random.choice(["com", "net", "org", "tr"])
    return f"{carrier_name.lower()}@kargo.{domain}"

def main():
    carriers = ["UPS", "PTTKargo", "Yurtici", "Surat", "MNG"]

    # File path
    os.makedirs('data/raw', exist_ok=True)
    output_file = 'data/raw/carrier.csv'

    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow(["carrier_id", "carrier_name", "carrier_phone", "carrier_email"])

        # Write data rows
        for carrier_id, carrier_name in enumerate(carriers, start=1):
            carrier_phone = generate_phone()
            carrier_email = generate_email(carrier_name)

            writer.writerow([carrier_id, carrier_name, carrier_phone, carrier_email])

    print(f"Carrier data successfully written to {output_file}")

if __name__ == "__main__":
    main()
