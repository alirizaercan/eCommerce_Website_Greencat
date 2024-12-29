# backend/controllers/address_controller.py
from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService
from utils.database import Database
import logging

logger = logging.getLogger(__name__)
address_controller = Blueprint('addresses', __name__)
db = Database()

@address_controller.route('/customer/<int:customer_id>/addresses', methods=['GET', 'POST'])
def handle_customer_addresses(customer_id):
    logger.info(f"Handling {request.method} request for customer {customer_id}")
    session = db.get_session()
    try:
        service = CustomerService(session)
        
        if request.method == 'POST':
            data = request.get_json()
            logger.debug(f"Received address data: {data}")
            
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400

            # Map frontend fields to backend fields
            address_data = {
                'customer_id': customer_id,
                'address_line1': data.get('address_line1'),
                'address_line2': data.get('address_line2'),
                'city': data.get('city'),
                'postal_code': data.get('postal_code'),
                'country': data.get('country', 'Türkiye'),
                'phone_number': data.get('phone_number'),
                'address_type': data.get('address_type', 'HOME')
            }

            # Validate required fields
            required_fields = ['address_line1', 'city', 'postal_code', 'phone_number']
            missing_fields = [field for field in required_fields if not address_data.get(field)]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400

            result = service.create_address(customer_id, address_data)
            return jsonify({'success': True, 'address': result}), 201

        # GET method
        addresses = service.get_customer_addresses(customer_id)
        return jsonify({'success': True, 'addresses': addresses}), 200

    except Exception as e:
        logger.error(f"Address controller error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        session.close()

@address_controller.route('/addresses/<int:address_id>', methods=['PUT', 'DELETE'])
def handle_address(address_id):
    session = db.get_session()
    try:
        service = CustomerService(session)
        
        if request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400

            result = service.update_address(address_id, data)
            if result:
                return jsonify({'success': True, 'address': result.to_dict()}), 200
            return jsonify({'success': False, 'error': 'Address not found'}), 404
            
        elif request.method == 'DELETE':
            result = service.delete_address(address_id)
            if result:
                return jsonify({'success': True, 'message': 'Address deleted'}), 200
            return jsonify({'success': False, 'error': 'Address not found'}), 404
            
    except Exception as e:
        logger.error(f"Address handling error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        session.close()