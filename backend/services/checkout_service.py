from models.customer_adress import CustomerAddress
from models.cart_item import CartItem
from models.order_details import OrderDetails
from services.payment_service import PaymentService
from sqlalchemy.orm import Session
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class CheckoutService:
    def __init__(self, session, payment_service):
        self.db_session = session
        self.payment_service = payment_service
        
        
    def validate_checkout(self, customer_id: int, session_id: int):
        try:
            # Validate customer exists
            if not customer_id:
                raise ValueError("Customer ID is required")

            # Get addresses
            addresses = self.db_session.query(CustomerAddress)\
                .filter(CustomerAddress.customer_id == customer_id)\
                .all()

            # Get cart items
            cart_items = self.db_session.query(CartItem)\
                .filter(CartItem.session_id == session_id)\
                .all()

            if not cart_items:
                return {
                    'success': False,
                    'error': 'Cart is empty'
                }

            cart_summary = self._calculate_cart_summary(cart_items)

            return {
                'success': True,
                'addresses': [addr.to_dict() for addr in addresses],
                'has_items': True,
                'cart_summary': cart_summary
            }

        except Exception as e:
            logger.error(f"Checkout validation error: {e}", exc_info=True)
            raise

    def process_checkout(self, customer_id: int, session_id: int, address_id: int, payment: dict):
        try:
            # Create order first
            cart_items = self.db_session.query(CartItem)\
                .filter(CartItem.session_id == session_id)\
                .all()
                
            cart_summary = self._calculate_cart_summary(cart_items)
            
            # Create order
            order = OrderDetails(
                customer_id=customer_id,
                total=cart_summary['total'],
                tax=cart_summary['tax'],
                order_status='PENDING'
            )
            
            self.db_session.add(order)
            self.db_session.flush()

            # Process payment with order_id
            payment_data = {
                'order_id': order.order_id,
                'amount': float(payment['amount']),
                'card_number': str(payment['card_number']),
                'card_holder': payment['card_holder'],
                'expiry_date': payment['expiry_date'],
                'cvv': payment['cvv']
            }

            payment_result = self.payment_service.process_payment(payment_data)
            
            if payment_result['success']:
                order.status = 'CONFIRMED'
                self.db_session.commit()
                
                return {
                    'success': True,
                    'order': order.to_dict()
                }
                
            raise ValueError("Payment failed")
        
        except Exception as e:
            self.db_session.rollback()
            raise


    def _calculate_cart_summary(self, cart_items):
        try:
            items = []
            subtotal = 0
            total_tax = 0
            
            for item in cart_items:
                product = item.product
                # Calculate base price
                unit_price = float(product.price)
                
                # Apply discount if exists
                if product.discount:
                    discount = float(product.discount.discount_percentage) / 100
                    unit_price = unit_price * (1 - discount)
                
                item_subtotal = unit_price * item.quantity
                item_tax = float(product.tax) * item.quantity
                
                items.append({
                    'id': item.cart_item_id,
                    'quantity': item.quantity,
                    'product': product.as_dict(),
                    'subtotal': item_subtotal,
                    'tax': item_tax
                })
                
                subtotal += item_subtotal
                total_tax += item_tax

            total = subtotal + total_tax

            return {
                'items': items,
                'subtotal': round(subtotal, 2),
                'tax': round(total_tax, 2),
                'total': round(total, 2),
                'total_items': sum(item['quantity'] for item in items)
            }
        except Exception as e:
            logger.error(f"Cart summary calculation error: {e}", exc_info=True)
            raise
        
    def get_checkout_summary(self, customer_id, session_id):
        cart_items = self.db_session.query(CartItem)\
            .filter(CartItem.session_id == session_id)\
            .all()

        subtotal = sum(Decimal(str(item.product.price)) * item.quantity for item in cart_items)
        tax = subtotal * Decimal('0.18')
        total = subtotal + tax

        return {
            'success': True,
            'summary': {
                'items': [item.to_dict() for item in cart_items],
                'subtotal': float(subtotal),
                'tax': float(tax),
                'total': float(total)
            }
        }