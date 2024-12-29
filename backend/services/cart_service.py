# backend/services/cart_service.py
from sqlalchemy.exc import SQLAlchemyError
from models.cart_item import CartItem
from models.product import Product
from utils.database import Database
from models.shopping_session import ShoppingSession
import logging

logger = logging.getLogger(__name__)

class CartService:
    def __init__(self, session=None):
        self.db = Database()
        self.session = session if session else self.db.get_session()
        
    def add_item_to_cart(self, session_id, product_id, quantity=1):
        try:
            # Validate session exists
            session = self.session.query(ShoppingSession).filter_by(session_id=session_id).first()
            if not session:
                raise ValueError("Invalid session ID")
                
            # Check product exists
            product = self.session.query(Product).filter_by(product_id=product_id).first()
            if not product:
                raise ValueError("Product not found")
                
            # Check existing cart item
            existing_item = self.session.query(CartItem).filter_by(
                session_id=session_id,
                product_id=product_id
            ).first()

            if existing_item:
                existing_item.quantity += quantity
                cart_item = existing_item
            else:
                cart_item = CartItem(
                    session_id=session_id,
                    product_id=product_id,
                    quantity=quantity
                )
                self.session.add(cart_item)

            self.session.commit()
            return self.get_cart_item_with_product(cart_item.cart_item_id)
                
        except Exception as e:
            self.session.rollback()
            raise e

    def get_cart_item_with_product(self, cart_item_id):
        cart_item = self.session.query(CartItem)\
            .join(Product)\
            .filter(CartItem.cart_item_id == cart_item_id)\
            .first()
        return cart_item.to_dict() if cart_item else None
    
    def get_cart_items(self, session_id):
        """Get all cart items with product details"""
        cart_items = self.session.query(CartItem)\
            .join(Product)\
            .filter(CartItem.session_id == session_id)\
            .all()
        
        result = []
        for item in cart_items:
            product = item.product
            item_dict = {
                'cart_item_id': item.cart_item_id,
                'quantity': item.quantity,
                'product': {
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'price': float(product.price),
                    'tax': float(product.tax),
                    'image_url': product.images[0].image_url if product.images else None,
                    'category_name': product.category.category_name if product.category else None,
                    'discount': {
                        'discount_percentage': product.discount.discount_percentage
                    } if product.discount else None
                },
                'subtotal': float(product.price) * item.quantity,
                'tax_amount': float(product.tax) * item.quantity
            }
            result.append(item_dict)
        
        return result

    def update_cart_item(self, cart_item_id, quantity):
        cart_item = self.session.query(CartItem)\
            .filter(CartItem.cart_item_id == cart_item_id)\
            .first()
        if cart_item:
            cart_item.quantity = quantity
            self.session.commit()
            return cart_item.as_dict()
        return None

    def delete_cart_item(self, cart_item_id):
        try:
            cart_item = self.session.query(CartItem)\
                .join(Product)\
                .filter(CartItem.cart_item_id == cart_item_id)\
                .first()

            if not cart_item:
                logger.warning(f"Cart item {cart_item_id} not found")
                return False

            # Update session total
            session = self.session.query(ShoppingSession)\
                .filter(ShoppingSession.session_id == cart_item.session_id)\
                .first()

            if session:
                product = cart_item.product
                item_total = float(product.price) * cart_item.quantity
                session.total = max(0, float(session.total) - item_total)

            self.session.delete(cart_item)
            self.session.commit()
            
            return True

        except SQLAlchemyError as e:
            logger.error(f"Database error deleting cart item: {e}")
            self.session.rollback()
            raise

    def get_cart_total(self, session_id):
        """Sepet toplamını hesaplar."""
        items = self.get_cart_items(session_id)
        return sum(item['product']['price'] * item['quantity'] for item in items)