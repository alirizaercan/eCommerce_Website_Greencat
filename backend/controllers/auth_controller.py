# backend/controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from services.customer_service import (
    register_customer, 
    login_customer, 
    get_customer_by_id, 
    update_customer, 
    delete_customer
)

auth_controller = Blueprint('auth', __name__)

@auth_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    required_fields = ["first_name", "last_name", "username", "email", "password", "phone_number"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    customer = register_customer(
        data['first_name'], 
        data['last_name'], 
        data['username'], 
        data['email'], 
        data['password'], 
        data['phone_number']
    )

    if customer:
        return jsonify({"message": "Registration successful"}), 201
    return jsonify({"message": "Username, email, or phone number already taken"}), 409

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "password")):
        return jsonify({"message": "Missing username or password"}), 400

    customer = login_customer(data['username'], data['password'])
    if customer:
        return jsonify({"message": "Login successful", "customer_id": customer.customer_id}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@auth_controller.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    if customer:
        return jsonify({
            "customer_id": customer.customer_id,
            "username": customer.username,
            "email": customer.email,
            "phone_number": customer.phone_number
        }), 200
    return jsonify({"message": "Customer not found"}), 404

@auth_controller.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer_details(customer_id):
    data = request.get_json()
    updated_customer = update_customer(customer_id, **data)
    if updated_customer:
        return jsonify({"message": "Customer updated successfully"}), 200
    return jsonify({"message": "Customer not found"}), 404

@auth_controller.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer_route(customer_id):
    success = delete_customer(customer_id)
    if success:
        return jsonify({"message": "Customer deleted successfully"}), 200
    return jsonify({"message": "Customer not found"}), 404
