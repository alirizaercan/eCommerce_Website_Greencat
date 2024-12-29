# backend/controllers/order_controller.py
# backend/controllers/order_controller.py
from flask import Blueprint, request, jsonify, current_app
from utils.database import Database
from services.order_service import OrderService
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any

order_controller = Blueprint('order_controller', __name__)
db = Database()

@order_controller.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer_orders(customer_id: int):
    db_session = db.get_session()
    try:
        if not customer_id:
            return jsonify({'error': 'Customer ID is required'}), 400

        order_service = OrderService(db_session)
        orders = order_service.get_customer_orders(customer_id)
        return jsonify(orders), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting orders: {str(e)}")
        return jsonify({'error': f'Failed to fetch orders: {str(e)}'}), 500
    finally:
        db_session.close()

@order_controller.route('/<int:order_id>', methods=['GET'])
def get_order_details(order_id: int):
    try:
        if not order_id:
            return jsonify({'error': 'Order ID is required'}), 400

        order_service = OrderService(db.session)
        order = order_service.get_order_by_id(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
            
        return jsonify(order.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Error getting order details: {str(e)}")
        return jsonify({'error': 'Failed to fetch order details'}), 500

@order_controller.route('', methods=['POST'])
def create_order_with_items():
    db_session = db.get_session()
    try:
        data: Dict[str, Any] = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_id', 'total', 'tax', 'order_status', 'payment_id', 'items']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        order_service = OrderService(db_session)
        order = order_service.create_order_with_items(
            customer_id=data['customer_id'],
            total=data['total'],
            tax=data['tax'],
            order_status=data['order_status'],
            payment_id=data['payment_id'],
            items=data['items']
        )
        return jsonify(order.to_dict()), 201

    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()
# Order Routes
@order_controller.route('/', methods=['GET'])
def get_all_orders():
    """Get all orders"""
    try:
        order_service = OrderService(db.session)
        orders = order_service.get_all_orders()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_controller.route('', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        order_service = OrderService(db.session)
        order = order_service.create_order(data)
        return jsonify(order.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_controller.route('/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    try:
        order_service = OrderService(db.session)
        order = order_service.get_order_by_id(order_id)
        if order:
            return jsonify(order.to_dict()), 200
        return jsonify({'message': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_controller.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id: int):
    """Update an existing order"""
    db_session = db.get_session()
    try:
        data = request.get_json()
        order_service = OrderService(db_session)
        order = order_service.update_order(
            order_id, data['total'], data['tax'], data['order_status'], data['payment_id']
        )
        if order:
            return jsonify(order.to_dict()), 200
        return jsonify({'message': 'Order not found'}), 404
    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

@order_controller.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id: int):
    """Delete an order"""
    db_session = db.get_session()
    try:
        order_service = OrderService(db_session)
        order = order_service.delete_order(order_id)
        if order:
            return jsonify({'message': 'Order deleted'}), 200
        return jsonify({'message': 'Order not found'}), 404
    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

# Order Item Routes
@order_controller.route('/<int:order_id>/items', methods=['POST'])
def add_order_item(order_id):
    db_session = db.get_session()
    try:
        data = request.get_json()
        order_service = OrderService(db_session)
        order_item = order_service.add_order_item(
            order_id, data['product_id'], data['quantity']
        )
        return jsonify(order_item.to_dict()), 201
    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

@order_controller.route('/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    try:
        order_service = OrderService(db.session)
        order_items = order_service.get_order_items(order_id)
        return jsonify([item.to_dict() for item in order_items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_controller.route('/order_items/<int:order_item_id>', methods=['PUT'])
def update_order_item(order_item_id):
    db_session = db.get_session()
    try:
        data = request.get_json()
        order_service = OrderService(db_session)
        order_item = order_service.update_order_item(order_item_id, data['quantity'])
        if order_item:
            return jsonify(order_item.to_dict()), 200
        return jsonify({'message': 'Order item not found'}), 404
    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

@order_controller.route('/order_items/<int:order_item_id>', methods=['DELETE'])
def delete_order_item(order_item_id):
    db_session = db.get_session()
    try:
        order_service = OrderService(db_session)
        order_item = order_service.delete_order_item(order_item_id)
        if order_item:
            return jsonify({'message': 'Order item deleted'}), 200
        return jsonify({'message': 'Order item not found'}), 404
    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()
    
@order_controller.route('/<int:order_id>/summary', methods=['GET'])
def get_order_summary(order_id: int):
    """Get summary of a specific order"""
    try:
        order_service = OrderService(db.session)
        summary = order_service.get_order_summary(order_id)
        if summary:
            return jsonify(summary), 200
        return jsonify({'message': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500