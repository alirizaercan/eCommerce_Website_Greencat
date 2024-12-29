# backend/controllers/carrier_controller.py
from flask import Blueprint, request, jsonify
from utils.database import Database
from models.carrier import Carrier
from services.carrier_service import CarrierService

carrier_controller = Blueprint('carrier_controller', __name__)
db = Database()

@carrier_controller.route('/order/<int:order_id>/carrier', methods=['GET'])
def get_order_carrier(order_id):
    try:
        carrier = CarrierService.assign_random_carrier()
        return jsonify({'carrier_name': carrier}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@carrier_controller.route('/carriers', methods=['POST'])
def create_carrier():
    data = request.get_json()
    carrier_service = CarrierService(db.session)
    carrier = carrier_service.create_carrier(data['carrier_name'], data['carrier_phone'], data['carrier_email'])
    return jsonify(carrier), 201

@carrier_controller.route('/carriers', methods=['GET'])
def get_all_carriers():
    carrier_service = CarrierService(db.session)
    carriers = carrier_service.get_all_carriers()
    return jsonify(carriers), 200

@carrier_controller.route('/carriers/<int:carrier_id>', methods=['GET'])
def get_carrier_by_id(carrier_id):
    carrier_service = CarrierService(db.session)
    carrier = carrier_service.get_carrier_by_id(carrier_id)
    if carrier:
        return jsonify(carrier), 200
    return jsonify({'message': 'Carrier not found'}), 404

@carrier_controller.route('/carriers/<int:carrier_id>', methods=['PUT'])
def update_carrier(carrier_id):
    data = request.get_json()
    carrier_service = CarrierService(db.session)
    carrier = carrier_service.update_carrier(carrier_id, data['carrier_name'], data['carrier_phone'], data['carrier_email'])
    if carrier:
        return jsonify(carrier), 200
    return jsonify({'message': 'Carrier not found'}), 404

@carrier_controller.route('/carriers/<int:carrier_id>', methods=['DELETE'])
def delete_carrier(carrier_id):
    carrier_service = CarrierService(db.session)
    carrier = carrier_service.delete_carrier(carrier_id)
    if carrier:
        return jsonify({'message': 'Carrier deleted'}), 200
    return jsonify({'message': 'Carrier not found'}), 404