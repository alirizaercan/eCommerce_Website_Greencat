# backend/controllers/auth_controller.py
from models.base import Base
from services.customer_service import CustomerService
from services.session_service import SessionService
from utils.database import Database
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging

auth_controller = Blueprint('auth', __name__)
customer_service = CustomerService()
db = Database()
logger = logging.getLogger(__name__)

@auth_controller.route('/register', methods=['POST'])
@cross_origin()
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), 400
        
        required_fields = ["first_name", "last_name", "username", "email", "password", "phone_number"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400
        
        customer = customer_service.register_customer(
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
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"error": "Registration failed"}), 500

@auth_controller.route('/login', methods=['POST'])
@cross_origin()
def login():
    db_session = db.get_session()
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ("username", "password")):
            return jsonify({"message": "Missing username or password"}), 400

        customer = customer_service.login_customer(data['username'], data['password'])
        if not customer:
            return jsonify({
                "message": "Invalid username or password",
                "isLoggedIn": False
            }), 401

        # Create shopping session
        session_service = SessionService(db_session)
        shopping_session = session_service.create_session(customer.customer_id, 0)
        
        if not shopping_session:
            logger.error(f"Failed to create session for customer {customer.customer_id}")
            return jsonify({"error": "Failed to create session"}), 500

        # Enhanced response data with all necessary information
        response_data = {
            "message": "Login successful",
            "isLoggedIn": True,
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "username": customer.username,
            "phone_number": customer.phone_number,
            "session_id": shopping_session.session_id
        }
        
        db_session.commit()
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        db_session.rollback()
        return jsonify({
            "error": "Login failed",
            "isLoggedIn": False
        }), 500
    finally:
        db_session.close()

@auth_controller.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        
        if not customer_id:
            return jsonify({
                "error": "Customer ID required",
                "isLoggedIn": True  # Still logged in since logout failed
            }), 400
            
        success = customer_service.logout_customer(customer_id)
        
        if success:
            return jsonify({
                "message": "Logged out successfully",
                "isLoggedIn": False
            }), 200
        return jsonify({
            "error": "Logout failed",
            "isLoggedIn": True  # Still logged in since logout failed
        }), 400
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({
            "error": str(e),
            "isLoggedIn": True  # Still logged in since logout failed
        }), 500

@auth_controller.route('/customer/<int:customer_id>', methods=['GET'])
@cross_origin()
def get_customer(customer_id):
    try:
        customer = customer_service.get_customer_by_id(customer_id)
        if customer:
            return jsonify({
                "customer_id": customer.customer_id,
                "username": customer.username,
                "email": customer.email,
                "phone_number": customer.phone_number,
                "first_name": customer.first_name,
                "last_name": customer.last_name
            }), 200
        return jsonify({"message": "Customer not found"}), 404
    except Exception as e:
        logger.error(f"Get customer error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@auth_controller.route('/customer/<int:customer_id>', methods=['PUT'])
@cross_origin()
def update_customer_details(customer_id):
    try:
        data = request.get_json()
        updated_customer = customer_service.update_customer(customer_id, **data)
        if updated_customer:
            return jsonify({"message": "Customer updated successfully"}), 200
        return jsonify({"message": "Customer not found"}), 404
    except Exception as e:
        logger.error(f"Update customer error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@auth_controller.route('/customer/<int:customer_id>', methods=['DELETE'])
@cross_origin()
def delete_customer_route(customer_id):
    try:
        success = customer_service.delete_customer(customer_id)
        if success:
            return jsonify({"message": "Customer deleted successfully"}), 200
        return jsonify({"message": "Customer not found"}), 404
    except Exception as e:
        logger.error(f"Delete customer error: {str(e)}")
        return jsonify({"error": str(e)}), 500