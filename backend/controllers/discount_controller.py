# backend/controllers/discount_controller.py
from flask import Blueprint, request, jsonify
from utils.database import Database
from services.discount_service import DiscountService

discount_controller = Blueprint('discount_controller', __name__)
db = Database()

@discount_controller.route('/discounts', methods=['POST'])
def create_discount():
    data = request.get_json()
    discount_service = DiscountService(db.session)
    discount = discount_service.create_discount(data['discount_name'], data['discount_description'], data['discount_percentage'], data['active'])
    return jsonify(discount), 201

@discount_controller.route('/discounts', methods=['GET'])
def get_all_discounts():
    discount_service = DiscountService(db.session)
    discounts = discount_service.get_all_discounts()
    return jsonify(discounts), 200

@discount_controller.route('/discounts/<int:discount_id>', methods=['GET'])
def get_discount_by_id(discount_id):
    discount_service = DiscountService(db.session)
    discount = discount_service.get_discount_by_id(discount_id)
    if discount:
        return jsonify(discount), 200
    return jsonify({'message': 'Discount not found'}), 404

@discount_controller.route('/discounts/<int:discount_id>', methods=['PUT'])
def update_discount(discount_id):
    data = request.get_json()
    discount_service = DiscountService(db.session)
    discount = discount_service.update_discount(discount_id, data['discount_name'], data['discount_description'], data['discount_percentage'], data['active'])
    if discount:
        return jsonify(discount), 200
    return jsonify({'message': 'Discount not found'}), 404

@discount_controller.route('/discounts/<int:discount_id>', methods=['DELETE'])
def delete_discount(discount_id):
    discount_service = DiscountService(db.session)
    discount = discount_service.delete_discount(discount_id)
    if discount:
        return jsonify({'message': 'Discount deleted'}), 200
    return jsonify({'message': 'Discount not found'}), 404