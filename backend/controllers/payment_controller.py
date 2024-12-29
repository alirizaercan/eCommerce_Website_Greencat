# backend/controllers/payment_controller.py
from flask import Blueprint, request, jsonify
from utils.database import Database
from services.payment_service import PaymentService
import logging

logger = logging.getLogger(__name__)
payment_controller = Blueprint('payment_controller', __name__)
db = Database()

@payment_controller.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    payment_service = PaymentService(db.session)
    payment = payment_service.create_payment(data['order_id'], data['amount'], data['tax'], data['provider'], data['status'])
    return jsonify(payment), 201

@payment_controller.route('/process', methods=['POST'])
def process_payment():
    try:
        data = request.get_json()
        service = PaymentService(db.get_session())
        
        result = service.process_payment(data)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@payment_controller.route('/payments', methods=['GET'])
def get_all_payments():
    payment_service = PaymentService(db.session)
    payments = payment_service.get_all_payments()
    return jsonify(payments), 200

@payment_controller.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id):
    payment_service = PaymentService(db.session)
    payment = payment_service.get_payment_by_id(payment_id)
    if payment:
        return jsonify(payment), 200
    return jsonify({'message': 'Payment not found'}), 404

@payment_controller.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    data = request.get_json()
    payment_service = PaymentService(db.session)
    payment = payment_service.update_payment(payment_id, data['amount'], data['tax'], data['provider'], data['status'])
    if payment:
        return jsonify(payment), 200
    return jsonify({'message': 'Payment not found'}), 404

@payment_controller.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment_service = PaymentService(db.session)
    payment = payment_service.delete_payment(payment_id)
    if payment:
        return jsonify({'message': 'Payment deleted'}), 200
    return jsonify({'message': 'Payment not found'}), 404