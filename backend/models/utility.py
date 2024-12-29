import os
import sys
import logging
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from models.base import Base
from models.admin_user import AdminUser
from models.carrier import Carrier
from models.cart_item import CartItem 
from models.category import Category
from models.customer import Customer
from models.customer_adress import CustomerAddress
from models.discount import Discount
from models.inventory import Inventory
from models.order_details import OrderDetails
from models.order_items import OrderItems
from models.payment_details import PaymentDetails
from models.product import Product
from models.product_image import ProductImage
from models.shopping_session import ShoppingSession
from utils.database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reset_all_sequences():
    """Reset auto-increment sequences for all models"""
    db = Database()
    session = db.get_session()
    
    models = [
        AdminUser, Carrier, CartItem, Category,
        Customer, CustomerAddress, Discount, Inventory,
        OrderDetails, OrderItems, PaymentDetails,
        Product, ProductImage, ShoppingSession
    ]
    
    try:
        for model in models:
            try:
                success = model.restart_sequence(session)
                logger.info(f"Reset sequence for {model.__tablename__}: {'Success' if success else 'Failed'}")
            except Exception as e:
                logger.error(f"Error resetting {model.__tablename__}: {str(e)}")
    except Exception as e:
        logger.error(f"Global error: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    reset_all_sequences()