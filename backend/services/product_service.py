# backend/services/product_service.py
from sqlalchemy.orm import Session
from models.product import Product
from models.category import Category
from models.inventory import Inventory
from models.discount import Discount
from models.product_image import ProductImage
from sqlalchemy.orm import joinedload

class ProductService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_product(self, product_data: dict) -> Product:
        # Verilen data'dan ürün bilgilerini alıyoruz
        product_name = product_data['product_name']
        product_description = product_data.get('product_description', '')
        sku = product_data['sku']
        category_id = product_data['category_id']
        inventory_id = product_data['inventory_id']
        price = product_data['price']
        tax = product_data.get('tax', 0.00)
        discount_id = product_data.get('discount_id', None)
        images = product_data.get('images', [])  # Resim URL'leri listesi
        
        # Yeni bir ürün nesnesi oluşturuyoruz
        new_product = Product(
            product_name=product_name,
            product_description=product_description,
            sku=sku,
            category_id=category_id,
            inventory_id=inventory_id,
            price=price,
            tax=tax,
            discount_id=discount_id
        )

        # Yeni ürünü veritabanına ekliyoruz
        self.db_session.add(new_product)
        self.db_session.commit()
        self.db_session.refresh(new_product)  # ID'yi alabilmek için ürünün yenilenmesi

        # Ürün resimlerini ekliyoruz
        for image_url in images:
            new_image = ProductImage(product_id=new_product.product_id, image_url=image_url)
            self.db_session.add(new_image)

        # Resimleri veritabanına kaydediyoruz
        self.db_session.commit()

        return new_product

    def update_product(self, product_id: int, update_data: dict) -> Product:
        # Ürünü ID'si ile buluyoruz
        product = self.db_session.query(Product).filter(Product.product_id == product_id).first()

        if not product:
            raise ValueError(f"Product with ID {product_id} not found.")

        # Ürünü güncelliyoruz
        for key, value in update_data.items():
            if hasattr(product, key):
                setattr(product, key, value)

        # Veritabanına kaydediyoruz
        self.db_session.commit()
        self.db_session.refresh(product)

        return product

    def delete_product(self, product_id: int) -> bool:
        # Silinecek ürünü buluyoruz
        product = self.db_session.query(Product).filter(Product.product_id == product_id).first()

        if not product:
            raise ValueError(f"Product with ID {product_id} not found.")

        # Ürünü siliyoruz
        self.db_session.delete(product)
        self.db_session.commit()

        return True

    def get_product_by_id(self, product_id: int) -> Product:
        # Ürünü ve ona ait resimleri ID ile alıyoruz
        product = self.db_session.query(Product).filter(Product.product_id == product_id).first()

        if not product:
            raise ValueError(f"Product with ID {product_id} not found.")
        
        # Ürünün resimlerini alıyoruz
        product_images = self.db_session.query(ProductImage).filter(ProductImage.product_id == product_id).all()
        product.images = product_images  # Resimleri ürün nesnesine ekliyoruz
        
        return product

    def get_all_products(self) -> list[Product]:
        return self.db_session.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.images),
            joinedload(Product.inventory),
            joinedload(Product.discount)
        ).all()

    def get_products_by_category(self, category_id: int) -> list[Product]:
        # Kategorisine göre ürünleri alıyoruz
        products = self.db_session.query(Product).filter(Product.category_id == category_id).all()

        # Her ürün için resimleri alıyoruz
        for product in products:
            product_images = self.db_session.query(ProductImage).filter(ProductImage.product_id == product.product_id).all()
            product.images = product_images

        return products

    def get_products_by_discount(self, discount_id: int) -> list[Product]:
        # İndirimli ürünleri alıyoruz
        products = self.db_session.query(Product).filter(Product.discount_id == discount_id).all()

        # Her ürün için resimleri alıyoruz
        for product in products:
            product_images = self.db_session.query(ProductImage).filter(ProductImage.product_id == product.product_id).all()
            product.images = product_images

        return products

    def apply_discount_to_product(self, product_id: int, discount_id: int) -> Product:
        # Ürüne indirim uyguluyoruz
        product = self.db_session.query(Product).filter(Product.product_id == product_id).first()

        if not product:
            raise ValueError(f"Product with ID {product_id} not found.")

        product.discount_id = discount_id

        # Veritabanına kaydediyoruz
        self.db_session.commit()
        self.db_session.refresh(product)

        return product


    def search_products(self, search_term: str) -> list[Product]:
        try:
            products = self.db_session.query(Product)\
                .options(
                    joinedload(Product.images),
                    joinedload(Product.category),
                    joinedload(Product.inventory),
                    joinedload(Product.discount)
                )\
                .filter(Product.product_name.ilike(f'%{search_term}%'))\
                .all()

            # Load images for each product
            for product in products:
                product_images = self.db_session.query(ProductImage)\
                    .filter(ProductImage.product_id == product.product_id)\
                    .all()
                product.images = product_images

            return products
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []