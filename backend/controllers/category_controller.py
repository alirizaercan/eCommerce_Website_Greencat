# backend/controllers/category_controller.py
from flask import Blueprint, jsonify
from sqlalchemy.orm import joinedload
from services.category_service import CategoryService
from models.product import Product
from utils.database import Database
import re

category_controller = Blueprint('category_controller', __name__)
db = Database()

def get_session():
    try:
        return db.get_session()
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None
    
def slugify(text):
    text = text.lower()
    return re.sub(r'[\s+]', '-', text)

@category_controller.route('/', methods=['GET'])
def get_all_categories():
    session = None
    try:
        session = get_session()
        if not session:
            return jsonify({"error": "Database connection failed"}), 500
            
        category_service = CategoryService()
        categories = category_service.get_all_categories()
        return jsonify(categories), 200
    except Exception as e:
        print(f"Error in get_all_categories: {str(e)}")
        return jsonify({"error": "Failed to fetch categories"}), 500
    finally:
        if session:
            session.close()

@category_controller.route('/<int:category_id>/products', methods=['GET'])
def get_category_products(category_id):
    session = None
    try:
        session = get_session()
        if not session:
            return jsonify({"error": "Database connection failed"}), 500

        # Query products with eager loading
        products = session.query(Product)\
            .filter(Product.category_id == category_id)\
            .options(
                joinedload(Product.images),
                joinedload(Product.category),
                joinedload(Product.inventory),
                joinedload(Product.discount)
            ).all()

        if not products:
            return jsonify([]), 200

        # Format product data consistently
        product_data = []
        for product in products:
            try:
                product_dict = product.as_dict()
                product_dict['image_url'] = product.images[0].image_url if product.images else None
                product_data.append(product_dict)
            except Exception as e:
                print(f"Error processing product {product.product_id}: {str(e)}")
                continue

        return jsonify(product_data), 200
    except Exception as e:
        print(f"Error in get_category_products: {str(e)}")
        return jsonify({"error": f"Failed to fetch products for category {category_id}"}), 500
    finally:
        if session:
            session.close()

@category_controller.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@category_controller.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500