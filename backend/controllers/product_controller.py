# backend/controllers/product_controller.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from services.product_service import ProductService
from utils.database import Database
from models.product import Product
from models.category import Category
import random

product_controller = Blueprint('product_controller', __name__)
db = Database()

# Veritabanı oturumu açmak için yardımcı fonksiyon
def get_session():
    """Get database session with error handling"""
    try:
        return db.get_session()
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None

@product_controller.route('/products', methods=['POST'])
def add_product():
    session = get_session()
    try:
        product_service = ProductService(session)
        product_data = request.json

        # Eğer category_id verilmemişse rastgele bir category_id seç
        if 'category_id' not in product_data or not product_data['category_id']:
            categories = session.query(Category).all()
            if categories:
                product_data['category_id'] = random.choice(categories).category_id

        new_product = product_service.add_product(product_data)
        return jsonify(new_product.as_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close(session)

@product_controller.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    session = get_session()
    try:
        product_service = ProductService(session)
        update_data = request.json
        updated_product = product_service.update_product(product_id, update_data)
        return jsonify(updated_product.as_dict()), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close(session)

@product_controller.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    session = get_session()
    try:
        product_service = ProductService(session)
        product_service.delete_product(product_id)
        session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close(session)

@product_controller.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    session = get_session()
    try:
        product_service = ProductService(session)
        product = product_service.get_product_by_id(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product.as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    finally:
        db.close(session)

@product_controller.route('/products', methods=['GET'])
def get_all_products():
    session = get_session()
    try:
        product_service = ProductService(session)
        products = product_service.get_all_products()
        return jsonify([product.as_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close(session)

@product_controller.route('/products/category/<int:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    session = get_session()
    try:
        product_service = ProductService(session)
        products = product_service.get_products_by_category(category_id)
        if not products:
            return jsonify({"error": "No products found in this category"}), 404
        return jsonify([product.as_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    finally:
        db.close(session)

@product_controller.route('/products/discount/<int:discount_id>', methods=['GET'])
def get_products_by_discount(discount_id):
    session = get_session()
    try:
        product_service = ProductService(session)
        products = product_service.get_products_by_discount(discount_id)
        if not products:
            return jsonify({"error": "No products found with this discount"}), 404
        return jsonify([product.as_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    finally:
        db.close(session)

@product_controller.route('/products/<int:product_id>/apply_discount/<int:discount_id>', methods=['PUT'])
def apply_discount_to_product(product_id, discount_id):
    session = get_session()
    try:
        product_service = ProductService(session)
        product = product_service.apply_discount_to_product(product_id, discount_id)
        if not product:
            return jsonify({"error": "Product or discount not found"}), 404
        return jsonify(product.as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close(session)

@product_controller.route('/random', methods=['GET'])
def get_random_products():
    session = None
    try:
        session = get_session()
        if not session:
            return jsonify({"error": "Database connection failed"}), 500
            
        product_service = ProductService(session)
        
        # Get products with eager loading of images
        query = session.query(Product)\
            .options(
                joinedload(Product.images),
                joinedload(Product.category),
                joinedload(Product.inventory),
                joinedload(Product.discount)
            )
        products = query.all()
        
        if not products:
            return jsonify([]), 200
            
        sample_size = min(40, len(products))
        random_products = random.sample(list(products), sample_size)
        
        # Simplified product data with error handling
        product_data = []
        for product in random_products:
            try:
                product_dict = product.as_dict()
                product_dict['image_url'] = product.images[0].image_url if product.images else None
                product_data.append(product_dict)
            except Exception as e:
                print(f"Error processing product {product.product_id}: {str(e)}")
                continue
        
        return jsonify(product_data), 200
    except Exception as e:
        print(f"Error in get_random_products: {str(e)}")
        if session:
            session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if session:
            session.close()
            
@product_controller.route('/search', methods=['GET'])
def search_products():
    session = get_session()
    try:
        search_term = request.args.get('term', '')
        if not search_term:
            return jsonify([]), 200

        product_service = ProductService(session)
        products = product_service.search_products(search_term)
        
        return jsonify([
            {
                **product.as_dict(),
                'image_url': product.images[0].image_url if product.images else None
            } 
            for product in products
        ]), 200
    except Exception as e:
        print(f"Search endpoint error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if session:
            db.close(session)