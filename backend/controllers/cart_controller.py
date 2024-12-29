# backend/controllers/cart_controller.py
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from services.cart_service import CartService
from sqlalchemy.exc import SQLAlchemyError
from utils.database import Database

cart_controller = Blueprint('cart_controller', __name__)
db = Database()

@cart_controller.route('', methods=['POST'])
@cross_origin()
def add_item_to_cart():
    session = db.get_session()
    cart_service = CartService(session)
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        if not all(k in data for k in ['session_id', 'product_id']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        cart_item = cart_service.add_item_to_cart(
            data['session_id'],
            data['product_id'],
            data.get('quantity', 1)
        )
        return jsonify(cart_item), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@cart_controller.route('/<int:session_id>', methods=['GET'])
@cross_origin()
def get_cart_items(session_id):
    session = db.get_session()
    cart_service = CartService(session)
    
    try:
        items = cart_service.get_cart_items(session_id)
        if not items:
            return jsonify({'message': 'Cart is empty'}), 200
        return jsonify(items), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@cart_controller.route('/item/<int:cart_item_id>', methods=['PUT'])
@cross_origin()
def update_cart_item(cart_item_id):
    try:
        data = request.get_json()
        cart_service = CartService()
        cart_item = cart_service.update_cart_item(cart_item_id, data['quantity'])
        if cart_item:
            return jsonify(cart_item), 200
        return jsonify({'message': 'Cart item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_controller.route('/item/<int:cart_item_id>', methods=['DELETE'])
@cross_origin()
def delete_cart_item(cart_item_id):
    session = db.get_session()
    cart_service = CartService(session)
    
    try:
        success = cart_service.delete_cart_item(cart_item_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Item removed successfully',
                'cart_item_id': cart_item_id
            }), 200
        return jsonify({
            'success': False,
            'message': 'Item not found'
        }), 404
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    finally:
        session.close()

@cross_origin()
def get_cart_total(session_id):
    try:
        cart_service = CartService()
        total = cart_service.get_cart_total(session_id)
        return jsonify({'total': float(total)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@cart_controller.route('/<int:session_id>/summary', methods=['GET'])
@cross_origin()
def get_cart_summary(session_id):
    session = db.get_session()
    cart_service = CartService(session)
    
    try:
        items = cart_service.get_cart_items(session_id)
        total = cart_service.get_cart_total(session_id)
        
        summary = {
            'items': items,
            'total_items': sum(item['quantity'] for item in items),
            'subtotal': sum(item['subtotal'] for item in items),
            'total_tax': sum(item['tax_amount'] for item in items),
            'total': total
        }
        
        return jsonify(summary), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()