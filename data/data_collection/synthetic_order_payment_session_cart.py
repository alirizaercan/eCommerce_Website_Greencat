import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Constants
total_orders = 5000
max_products_per_order = 5
product_id_range = (1, 1000)
customer_id_range = (1, 1000)
payment_id_range = (1, 5000)
price_min = 200
price_max = 50000
providers = ["VISA", "MASTERCARD", "TROY"]
statuses = ["Success", "Pending", "Failed"]
order_statuses = ["Pending", "Shipped", "Delivered", "Cancelled"]

# Shopping specific constants
total_shopping_sessions = 7500  # More sessions than orders
abandoned_cart_ratio = 0.3  # 30% of carts are abandoned
max_items_per_cart = 8
product_price_ranges = {
    'low': (50, 500),
    'medium': (501, 2000),
    'high': (2001, 10000)
}

# File paths
order_details_path = "data/raw/order_details.csv"
order_items_path = "data/raw/order_items.csv"
payment_details_path = "data/raw/payment_details.csv"
shopping_session_path = "data/raw/shopping_session.csv"
cart_item_path = "data/raw/cart_item.csv"

def random_timestamp():
    """Generates a random timestamp between two dates"""
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86399)
    return start_date + timedelta(days=random_days, seconds=random_seconds)

def generate_product_price():
    """Generates a product price with weighted categories"""
    price_category = random.choices(
        ['low', 'medium', 'high'],
        weights=[0.6, 0.3, 0.1]  # 60% low, 30% medium, 10% high
    )[0]
    
    min_price, max_price = product_price_ranges[price_category]
    return round(random.uniform(min_price, max_price), 2)

def simulate_shopping_behavior():
    """Simulates different shopping patterns"""
    patterns = [
        {'items': (1, 2), 'weight': 0.4},    # Quick purchase
        {'items': (3, 5), 'weight': 0.4},    # Normal shopping
        {'items': (6, 8), 'weight': 0.2}     # Large cart
    ]
    
    chosen_pattern = random.choices(
        patterns,
        weights=[p['weight'] for p in patterns]
    )[0]
    
    return random.randint(*chosen_pattern['items'])

def generate_shopping_sessions():
    """Generates shopping session and cart item data"""
    shopping_session_data = []
    cart_item_data = []
    cart_item_id = 1
    
    # Track product prices for consistency
    product_prices = {}

    # Generate shopping session data
    for session_id in range(1, total_shopping_sessions + 1):
        customer_id = random.randint(*customer_id_range)
        created_at = random_timestamp()
        
        # Simulate realistic session duration (5 min to 2 hours)
        session_duration = timedelta(minutes=random.randint(5, 120))
        modified_at = created_at + session_duration
        
        # Determine number of items based on shopping behavior
        num_items = simulate_shopping_behavior()
        session_total = 0
        
        # Generate cart items
        for _ in range(num_items):
            product_id = random.randint(*product_id_range)
            
            # Ensure consistent pricing for products
            if product_id not in product_prices:
                product_prices[product_id] = generate_product_price()
            
            product_price = product_prices[product_id]
            quantity = random.randint(1, 5)  # Most people buy 1-5 of an item
            
            # Item timing within session
            item_add_time = random.randint(1, int(session_duration.total_seconds() // 2))
            created_at_item = created_at + timedelta(seconds=item_add_time)
            modified_at_item = created_at_item + timedelta(minutes=random.randint(1, 30))

            cart_item_data.append([
                cart_item_id,
                session_id,  # This session_id will match with the shopping session
                product_id,
                quantity,
                created_at_item,
                modified_at_item
            ])
            
            session_total += product_price * quantity
            cart_item_id += 1

        # Simulate abandoned carts with lower totals
        if random.random() < abandoned_cart_ratio:
            session_total *= random.uniform(0.1, 0.8)  # Partially filled carts

        shopping_session_data.append([
            session_id,
            customer_id,
            round(session_total, 2),
            created_at,
            modified_at
        ])

    return shopping_session_data, cart_item_data

def generate_orders_and_payments():
    """Generates order and payment data"""
    order_details_data = []
    order_items_data = []
    payment_details_data = []
    order_item_id = 1

    for order_id in range(1, total_orders + 1):
        customer_id = random.randint(*customer_id_range)
        total = round(random.uniform(price_min, price_max), 2)
        tax = round(total * 0.18, 2)
        payment_id = order_id
        created_at = random_timestamp()
        modified_at = created_at + timedelta(minutes=random.randint(1, 1440))
        order_status = random.choice(order_statuses)

        order_details_data.append([
            order_id, customer_id, total, tax, order_status, payment_id, created_at, modified_at
        ])

        provider = random.choice(providers)
        status = random.choice(statuses)

        payment_details_data.append([
            payment_id, order_id, total, tax, provider, status, created_at, modified_at
        ])

        num_items = random.randint(1, max_products_per_order)
        for _ in range(num_items):
            product_id = random.randint(*product_id_range)
            quantity = random.randint(1, 10)
            created_at_item = created_at
            modified_at_item = modified_at

            order_items_data.append([
                order_item_id, order_id, product_id, quantity, created_at_item, modified_at_item
            ])

            order_item_id += 1

    return order_details_data, order_items_data, payment_details_data

def write_to_csv(file_path, header, data):
    """Writes data to a CSV file"""
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

def main():
    """Main function to generate all data and save to CSV files"""
    # Generate all data
    order_details_data, order_items_data, payment_details_data = generate_orders_and_payments()
    shopping_session_data, cart_item_data = generate_shopping_sessions()

    # Write all data to CSV files
    write_to_csv(order_details_path,
                 ["order_id", "customer_id", "total", "tax", "order_status", "payment_id", "created_at", "modified_at"],
                 order_details_data)

    write_to_csv(order_items_path,
                 ["order_item_id", "order_id", "product_id", "quantity", "created_at", "modified_at"],
                 order_items_data)

    write_to_csv(payment_details_path,
                 ["payment_id", "order_id", "amount", "tax", "provider", "status", "created_at", "modified_at"],
                 payment_details_data)

    write_to_csv(shopping_session_path,
                 ["session_id", "customer_id", "total", "created_at", "modified_at"],
                 shopping_session_data)

    write_to_csv(cart_item_path,
                 ["cart_item_id", "session_id", "product_id", "quantity", "created_at", "modified_at"],
                 cart_item_data)

    print("Tüm veriler başarıyla oluşturuldu ve kaydedildi.")

if __name__ == "__main__":
    main()
