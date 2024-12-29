import csv
import random
from datetime import datetime, timedelta
from faker import Faker
from werkzeug.security import generate_password_hash

# Initialize Faker with Turkish locale
fake = Faker('tr_TR')

# Constants
TOTAL_CUSTOMERS = 1000
STARTING_CUSTOMER_ID = 3
MAX_LOGIN_ATTEMPTS = 10
MAX_WRONG_LOGIN_ATTEMPTS = 5

# File paths
customer_path = "data/raw/customer.csv"
customer_address_path = "data/raw/customer_address.csv"

# Turkish cities with weights
turkish_cities = [
    ("İstanbul", 0.25),
    ("Ankara", 0.15),
    ("İzmir", 0.12),
    ("Bursa", 0.08),
    ("Antalya", 0.07),
    ("Adana", 0.05),
    ("Konya", 0.05),
    ("Gaziantep", 0.05),
    ("Kocaeli", 0.03),
    ("Mersin", 0.03),
    ("Eskişehir", 0.03),
    ("Samsun", 0.02),
    ("Denizli", 0.02),
    ("Trabzon", 0.02),
    ("Malatya", 0.02),
    ("Van", 0.01)
]

def generate_unique_username(existing_usernames, first_name, last_name):
    """Generate a unique username based on first and last name"""
    base = f"{first_name.lower()}{last_name.lower()}"
    username = base
    counter = 1
    
    while username in existing_usernames:
        username = f"{base}{counter}"
        counter += 1
    
    return username

def generate_unique_email(existing_emails, first_name, last_name):
    """Generate a unique email address"""
    domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']
    base = f"{first_name.lower()}.{last_name.lower()}"
    email = f"{base}@{random.choice(domains)}"
    counter = 1
    
    while email in existing_emails:
        email = f"{base}{counter}@{random.choice(domains)}"
        counter += 1
    
    return email

def generate_valid_phone_number():
    """Generate a phone number that fits within VARCHAR(20)"""
    # Turkish mobile number format: +90 5XX XXX XXXX
    operator_codes = ['50', '53', '54', '55', '56']
    operator = random.choice(operator_codes)
    subscriber = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    phone = f"+90{operator}{subscriber}"
    return phone[:20]  # Ensure it fits within VARCHAR(20)

def random_timestamp(start_year=2020):
    """Generate a random timestamp from start_year to now"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(2024, 1, 1)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def generate_customer_data():
    """Generate customer and address data"""
    customers = []
    addresses = []
    existing_usernames = set()
    existing_emails = set()
    existing_phones = set()
    
    for i in range(TOTAL_CUSTOMERS):
        customer_id = i + STARTING_CUSTOMER_ID
        
        # Generate basic info
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = generate_unique_username(existing_usernames, first_name, last_name)
        email = generate_unique_email(existing_emails, first_name, last_name)
        
        # Generate password using werkzeug's generate_password_hash
        raw_password = fake.password(length=12)
        hashed_password = generate_password_hash(raw_password)
        
        # Generate unique phone number
        while True:
            phone = generate_valid_phone_number()
            if phone not in existing_phones:
                existing_phones.add(phone)
                break
        
        # Generate timestamps
        created_at = random_timestamp()
        modified_at = created_at + timedelta(days=random.randint(0, 365))
        
        # Create customer record
        customer = [
            customer_id,
            first_name,
            last_name,
            username,
            email,
            hashed_password,
            phone,  # Using the same phone number for both tables
            random.randint(0, MAX_LOGIN_ATTEMPTS),
            random.randint(0, MAX_WRONG_LOGIN_ATTEMPTS),
            created_at,
            modified_at
        ]
        customers.append(customer)
        
        # Generate address for customer
        city, _ = random.choices(turkish_cities, weights=[w for _, w in turkish_cities])[0]
        
        address = [
            customer_id,  # Using same ID for address_id for simplicity
            customer_id,
            fake.street_address(),
            fake.random_element([fake.secondary_address(), None, None]),  # 33% chance of having secondary address
            city,
            fake.postcode(),
            "Türkiye",
            phone  # Using the same phone number as in customer table
        ]
        addresses.append(address)
        
        # Update tracking sets
        existing_usernames.add(username)
        existing_emails.add(email)
    
    return customers, addresses

def write_to_csv(file_path, header, data):
    """Write data to CSV file"""
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

def main():
    # Generate data
    print("Veri üretiliyor...")
    customers, addresses = generate_customer_data()
    
    # Define headers
    customer_header = [
        "customer_id", "first_name", "last_name", "username", "email",
        "password", "phone_number", "login_attempts", "wrong_login_attempts",
        "created_at", "modified_at"
    ]
    
    address_header = [
        "address_id", "customer_id", "address_line1", "address_line2",
        "city", "postal_code", "country", "phone_number"
    ]
    
    # Write to CSV files
    write_to_csv(customer_path, customer_header, customers)
    write_to_csv(customer_address_path, address_header, addresses)
    
    print(f"\nVeriler başarıyla oluşturuldu:")
    print(f"- Müşteri verileri: {customer_path}")
    print(f"- Adres verileri: {customer_address_path}")
    
    # Print sample data
    print("\nÖrnek müşteri verisi:")
    print(f"ID: {customers[0][0]}")
    print(f"Ad Soyad: {customers[0][1]} {customers[0][2]}")
    print(f"Email: {customers[0][4]}")
    print(f"Telefon: {customers[0][6]}")  # Show phone number in sample
    print(f"Şehir: {addresses[0][4]}")

if __name__ == "__main__":
    main()