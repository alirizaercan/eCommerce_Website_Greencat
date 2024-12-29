from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from services.checkout_service import CheckoutService
from services.payment_service import PaymentService
from utils.database import Database
import logging

checkout_controller = Blueprint('checkout', __name__)
db = Database()
logger = logging.getLogger(__name__)

@checkout_controller.route('/validate', methods=['POST'])
@cross_origin()
def validate_checkout():
    session = db.get_session()
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        session_id = data.get('session_id')

        if not all([customer_id, session_id]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
            
        payment_service = PaymentService(session)

        checkout_service = CheckoutService(session, payment_service)
        result = checkout_service.validate_checkout(customer_id, session_id)
        
        # Add cart summary to response
        cart_summary = result.get('cart_summary', {})
        return jsonify({
            'success': True,
            'addresses': result.get('addresses', []),
            'has_items': result.get('has_items', False),
            'summary': {
                'subtotal': cart_summary.get('subtotal', 0),
                'tax': cart_summary.get('tax', 0),
                'total': cart_summary.get('total', 0),
                'items': cart_summary.get('items', [])
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        session.close()

@checkout_controller.route('/process', methods=['POST'])
def process_checkout():
    session = db.get_session()
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Invalid or missing data")
        
        logger.info(f"Received checkout data: {data}")

        # Validate required fields
        required_fields = ['customer_id', 'session_id', 'address_id', 'payment']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            
        # Validate payment data
        payment_data = data.get('payment', {})
        required_payment_fields = ['amount', 'card_number', 'card_holder', 'expiry_date', 'cvv']
        for field in required_payment_fields:
            if field not in payment_data:
                raise ValueError(f"Missing required payment field: {field}")

        checkout_service = CheckoutService(
            session=session,
            payment_service=PaymentService(session)
        )

        result = checkout_service.process_checkout(
            customer_id=data['customer_id'],
            session_id=data['session_id'],
            address_id=data['address_id'],
            payment=payment_data
        )

        logger.info(f"Checkout result: {result}")
        return jsonify(result), 200

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        session.close()

        
@checkout_controller.route('/summary', methods=['GET'])
def get_checkout_summary():
    session = db.get_session()
    try:
        customer_id = request.args.get('customer_id')
        session_id = request.args.get('session_id')
        service = CheckoutService(session)
        summary = service.get_checkout_summary(customer_id, session_id)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
    