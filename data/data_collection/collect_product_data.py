from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, csv, os, random
from datetime import datetime

# Function to generate unique SKU for each product
def generate_sku():
    return f"TY-{''.join(random.choices('0123456789', k=6))}"

# Function to extract and format the price correctly
def extract_price(price_text):
    try:
        return round(float(price_text.replace('TL', '').replace('.', '').replace(',', '.').strip()), 2)
    except:
        return 0.0

# Scraping and inserting data into the appropriate CSV files
def scrape_url(driver, url, writer, img_writer, start_id, category_id):
    driver.get(url)
    time.sleep(5)
    products_processed = 0
    product_id = start_id
    inventory_id = start_id  # This will be used for Inventory ID
    image_id = start_id  # This will be used for Image ID
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    while products_processed < 100:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for card in soup.find_all('div', class_='p-card-wrppr'):
            if products_processed >= 100:
                break

            try:
                # Extract product information
                name = card.find('span', class_='prdct-desc-cntnr-name').text.strip()
                brand = card.find('span', class_='prdct-desc-cntnr-ttl').text.strip()
                price_div = card.find('div', class_='prc-box-dscntd')
                price = extract_price(price_div.text) if price_div else 0.0
                rating = float(card.find('span', class_='rating-score').text) if card.find('span', class_='rating-score') else 0.0
                review_count = int(card.find('span', class_='ratingCount').text.strip('()')) if card.find('span', class_='ratingCount') else 0

                # Inventory ID and Discount ID
                discount_id = random.choice(list(range(1, 6)))
                # Write product data to the CSV
                writer.writerow([
                    product_id,
                    name,
                    f"{brand} {name}",
                    generate_sku(),
                    category_id,
                    inventory_id,
                    round(price, 2),
                    round(price * 0.18, 2),  # Tax calculation (18%)
                    round(rating, 2),
                    review_count,
                    discount_id,
                    timestamp,
                    timestamp
                ])

                # Handle product images
                img_element = card.find('img', class_='p-card-img')
                if img_element and img_element.get('src'):
                    img_writer.writerow([image_id, product_id, img_element['src']])

                # Increment product ID, inventory ID, and image ID
                product_id += 1
                inventory_id += 1  # Increment inventory ID
                image_id += 1  # Increment image ID
                products_processed += 1

            except Exception as e:
                print(f"Error: {e}")
                continue

        # Scroll to the bottom to load more products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    return product_id, inventory_id, image_id

# Main function to orchestrate the scraping
def main():
    urls = {
        1: 'https://www.trendyol.com/sr?wc=108656,103665',
        2: 'https://www.trendyol.com/sr/ayakkabi-x-c114?fl=encoksatanurunler',
        3: 'https://www.trendyol.com/gida-ve-icecek-x-c103946',
        4: 'https://www.trendyol.com/diger-kisisel-bakim-urunleri-x-c104068',
        5: 'https://www.trendyol.com/kitap-x-c91',
        6: 'https://www.trendyol.com/spor-aletleri-x-c104192',
        7: 'https://www.trendyol.com/oyuncak-x-c90',
        8: 'https://www.trendyol.com/sr?wc=105085&qt=saglik&st=saglik&os=1',
        9: 'https://www.trendyol.com/sr?q=otomotiv&qt=otomotiv&st=otomotiv&os=1',
        10: 'https://www.trendyol.com/sr?wc=89%2C103799'
    }

    driver = webdriver.Chrome(options=Options())
    os.makedirs('data/raw', exist_ok=True)

    with open('data/raw/products.csv', 'w', newline='', encoding='utf-8') as f_prod, \
         open('data/raw/product_images.csv', 'w', newline='', encoding='utf-8') as f_img:
        
        prod_writer = csv.writer(f_prod)
        img_writer = csv.writer(f_img)
        
        # Write headers for product and image data
        prod_writer.writerow([
            "product_id", "product_name", "product_description", "sku", "category_id", "inventory_id", 
            "price", "tax", "rating", "review_count", "discount_id", "created_at", "modified_at"
        ])
        img_writer.writerow(['image_id', 'product_id', 'image_url'])

        current_product_id = 1
        current_inventory_id = 1
        current_image_id = 1

        for category_id, url in urls.items():
            print(f"Scraping category {category_id}...")
            current_product_id, current_inventory_id, current_image_id = scrape_url(driver, url, prod_writer, img_writer, current_product_id, category_id)

    driver.quit()
    print("Data extraction completed")

if __name__ == "__main__":
    main()
