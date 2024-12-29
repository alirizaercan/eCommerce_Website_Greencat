# backend/services/category_service.py
from utils.database import Database
from sqlalchemy.orm import joinedload
from models.category import Category
from models.product import Product

class CategoryService:
    def __init__(self):
        self.db = Database()

    def get_all_categories(self):
        try:
            with self.db.get_session() as session:
                categories = session.query(Category).all()
                return [category.as_dict() for category in categories]
        except Exception as e:
            print(f"Error in get_all_categories: {str(e)}")
            raise

    def get_products_by_category(self, category_id):
        try:
            with self.db.get_session() as session:
                products = session.query(Product)\
                    .filter(Product.category_id == category_id)\
                    .options(
                        joinedload(Product.images),
                        joinedload(Product.category),
                        joinedload(Product.inventory),
                        joinedload(Product.discount)
                    ).all()
                
                return [self._format_product(product) for product in products]
        except Exception as e:
            print(f"Error in get_products_by_category: {str(e)}")
            raise

    def _format_product(self, product):
        return {
            'product_id': product.product_id,
            'name': product.product_name,
            'description': product.product_description,
            'price': float(product.price),
            'image_url': product.images[0].image_url if product.images else None,
            'category_name': product.category.category_name if product.category else None,
            'discount': {
                'discount_percentage': product.discount.discount_percentage
            } if product.discount else None
        }