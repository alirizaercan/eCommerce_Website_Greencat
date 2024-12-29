import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        database_url = os.getenv("DATABASE_URL")
        self.connection = psycopg2.connect(database_url)
        self.cursor = self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

class CSVLoader:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def load_csv_to_table(self, csv_path, table_name, columns):
        try:
            print(f"\nLoading data into {table_name}...")
            data = pd.read_csv(csv_path)
            data = data.where(pd.notnull(data), None)
            
            # Batch commit için sayaç
            batch_size = 100
            commit_counter = 0

            for _, row in data.iterrows():
                try:
                    primary_key_column = columns[0]
                    primary_key_value = row[primary_key_column]

                    # Kayıt var mı kontrol et
                    select_query = sql.SQL("SELECT 1 FROM {table} WHERE {primary_key} = %s").format(
                        table=sql.Identifier(table_name),
                        primary_key=sql.Identifier(primary_key_column)
                    )
                    self.db_manager.execute_query(select_query, (primary_key_value,))
                    exists = self.db_manager.cursor.fetchone()

                    if exists:
                        print(f"Record with {primary_key_column}={primary_key_value} already exists in {table_name}. Skipping.")
                        continue

                    # Insert işlemi
                    values = [row[col] for col in columns]
                    placeholders = ", ".join(["%s"] * len(columns))
                    insert_query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values})").format(
                        table=sql.Identifier(table_name),
                        fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
                        values=sql.SQL(placeholders)
                    )
                    self.db_manager.execute_query(insert_query, values)
                    
                    commit_counter += 1
                    if commit_counter >= batch_size:
                        self.db_manager.commit()
                        commit_counter = 0

                except Exception as e:
                    self.db_manager.rollback()
                    print(f"Error inserting record into {table_name}: {str(e)}")
                    raise

            # Kalan kayıtları commit et
            if commit_counter > 0:
                self.db_manager.commit()

        except Exception as e:
            print(f"Error loading {table_name}: {str(e)}")
            raise

def main():
    db_manager = DatabaseManager()
    db_manager.connect()
    csv_loader = CSVLoader(db_manager)

    # Bağımlılık sırasına göre düzenlenmiş veri yükleme sırası
    data_mappings = [
        
        # Bağımsız Temel Tablolar
        ("data/raw/category.csv", "category", [
            "category_id", "category_name", "category_description", "created_at", "modified_at"
        ]),
        ("data/raw/inventory.csv", "inventory", [
            "inventory_id", "quantity", "created_at", "modified_at"
        ]),
        ("data/raw/discount.csv", "discount", [
            "discount_id", "discount_name", "discount_description", "discount_percentage", 
            "active", "created_at", "modified_at"
        ]),
        ("data/raw/carrier.csv", "carrier", [
            "carrier_id", "carrier_name", "carrier_phone", "carrier_email"
        ]),

        # Müşteri ve Temel Tablolar
        ("data/raw/customer.csv", "customer", [
            "customer_id", "first_name", "last_name", "username", "email", "password", 
            "phone_number", "login_attempts", "wrong_login_attempts", "created_at", "modified_at"
        ]),
        ("data/raw/customer_address.csv", "customer_address", [
            "address_id", "customer_id", "address_line1", "address_line2", "city", 
            "postal_code", "country", "phone_number"
        ]),

        # Ürün ve İlişkili Tablolar
        ("data/raw/products.csv", "product", [
            "product_id", "product_name", "product_description", "sku", "category_id", 
            "inventory_id", "price", "tax", "rating", "review_count", "discount_id", 
            "created_at", "modified_at"
        ]),
        ("data/raw/product_images.csv", "product_image", [
            "image_id", "product_id", "image_url"
        ]),

        # Oturum ve Sepet
        ("data/raw/shopping_session.csv", "shopping_session", [
            "session_id", "customer_id", "total", "created_at", "modified_at"
        ]),
        ("data/raw/cart_item.csv", "cart_item", [
            "cart_item_id", "session_id", "product_id", "quantity", "created_at", "modified_at"
        ]),

        # Sipariş ve Ödeme (Sıralama önemli)
        ("data/raw/order_details.csv", "order_details", [
            "order_id", "customer_id", "total", "tax", "order_status", "created_at", "modified_at"
        ]),
        ("data/raw/payment_details.csv", "payment_details", [
            "payment_id", "order_id", "amount", "tax", "provider", "status", "created_at", "modified_at"
        ]),
        ("data/raw/order_items.csv", "order_items", [
            "order_item_id", "order_id", "product_id", "quantity", "created_at", "modified_at"
        ])
    ]

    try:
        for csv_path, table_name, columns in data_mappings:
            csv_loader.load_csv_to_table(csv_path, table_name, columns)
            print(f"Successfully loaded {table_name}")
    except Exception as e:
        print(f"Error during data loading: {str(e)}")
    finally:
        db_manager.close()

if __name__ == "__main__":
    main()