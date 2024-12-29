from models.admin_user import AdminUser
from models.admin_type import AdminType
from models.order_details import OrderDetails
from models.order_items import OrderItems
from models.product import Product
from models.category import Category
from models.customer import Customer
from models.inventory import Inventory
from models.discount import Discount
from models.payment_details import PaymentDetails
from models.shopping_session import ShoppingSession
from models.customer_adress import CustomerAddress
from models.customer import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, desc
import logging
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import timedelta
import time
from dotenv import load_dotenv
import os
import time
import logging

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 1

class Database:
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.connect()
        
    

    def connect(self):
        if self.engine is None:
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError("DATABASE_URL not found in environment variables")
            
            retry_count = 0
            while retry_count < MAX_RETRIES:
                try:
                    self.engine = create_engine(database_url)
                    # Test connection
                    self.engine.connect()
                    Base.metadata.create_all(self.engine)
                    self.session_factory = scoped_session(sessionmaker(bind=self.engine))
                    break
                except SQLAlchemyError as e:
                    retry_count += 1
                    logger.warning(f"Database connection attempt {retry_count} failed: {str(e)}")
                    if retry_count >= MAX_RETRIES:
                        raise ValueError(f"Failed to connect to database after {MAX_RETRIES} attempts")
                    time.sleep(RETRY_DELAY)

    def get_session(self):
        if not self.session_factory:
            self.connect()
        try:
            session = self.session_factory()
            # Verify session
            session.query("1").first()
            return session
        except SQLAlchemyError as e:
            logger.error(f"Error creating session: {str(e)}")
            if session:
                session.rollback()
                session.close()
            raise

    def close(self, session):
        try:
            if session:
                session.close()
                self.session_factory.remove()
        except Exception as e:
            logger.error(f"Error closing session: {str(e)}")

class AdminService:
    def __init__(self, engine):
        """Initialize with engine instead of session"""
        if not engine:
            raise ValueError("Database engine cannot be None")
        
        self.engine = engine
        self.session_factory = scoped_session(sessionmaker(bind=engine))
        self.db_session = self.session_factory()
        self._ensure_admin_exists()

    def __del__(self):
        """Cleanup on deletion"""
        if self.db_session:
            self.db_session.close()
            self.session_factory.remove()
        
    def _initialize_session(self):
        """Initialize database session with retry logic"""
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                if hasattr(self, 'db_session') and self.db_session:
                    self.db_session.close()
                self.db_session = self.session_factory()
                # Verify connection
                self.db_session.query(AdminUser).first()
                logger.info("Database session initialized successfully")
                return
            except SQLAlchemyError as e:
                retry_count += 1
                logger.warning(f"Session initialization attempt {retry_count} failed: {str(e)}")
                if retry_count >= MAX_RETRIES:
                    raise ValueError(f"Failed to initialize session after {MAX_RETRIES} attempts")
                time.sleep(RETRY_DELAY)

    
    def _validate_session(self):
        """Validate session with retry logic"""
        if not self.db_session:
            raise ValueError("No database session available")
            
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                self.db_session.query(AdminUser).first()
                return True
            except SQLAlchemyError as e:
                retry_count += 1
                logger.warning(f"Session validation attempt {retry_count} failed: {str(e)}")
                
                if retry_count >= MAX_RETRIES:
                    self.db_session.rollback()
                    raise ValueError("Session validation failed after max retries")
                    
                time.sleep(RETRY_DELAY)
                
        return False

    def _ensure_admin_exists(self):
        """Ensure admin user exists in database"""
        try:
            self._validate_session()
            admin = self.db_session.query(AdminUser).filter_by(username='admin').first()
            if not admin:
                self.initialize_admin_types()
                self.initialize_admin_users()
                self.db_session.commit()
                logging.info("Admin users initialized successfully")
        except Exception as e:
            logging.error(f"Error ensuring admin exists: {str(e)}")
            if self.db_session:
                self.db_session.rollback()
            raise

    def initialize_admin_types(self):
        """Initialize default admin types"""
        admin_types = [
            AdminType("admin", "all"),
            AdminType("developer", "half-permission"),
            AdminType("seller", "limited-permission")
        ]
        for admin_type in admin_types:
            self.db_session.merge(admin_type)
        self.db_session.commit()

    def initialize_admin_users(self):
        """Initialize default admin users"""
        admin_users = [
            {
                "username": "admin",
                "password": generate_password_hash("admin123"),
                "first_name": "admin",
                "last_name": "admin",
                "type_id": 1
            },
            {
                "username": "developer",
                "password": generate_password_hash("developer123"),
                "first_name": "developer",
                "last_name": "developer",
                "type_id": 2
            },
            {
                "username": "seller",
                "password": generate_password_hash("seller123"),
                "first_name": "seller",
                "last_name": "seller",
                "type_id": 3
            }
        ]
        
        for user_data in admin_users:
            admin_user = AdminUser(**user_data)
            self.db_session.merge(admin_user)
        self.db_session.commit()

    def authenticate_admin(self, username, password):
        """Authenticate admin user and update last login"""
        try:
            self._validate_session()
            
            if not username or not password:
                raise ValueError("Username and password are required")

            admin_user = self.db_session.query(AdminUser).filter_by(username=username).first()
            if admin_user and check_password_hash(admin_user.password, password):
                admin_user.last_login = datetime.utcnow()
                self.db_session.commit()
                return admin_user
            return None

        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            if self.db_session:
                self.db_session.rollback()
            raise

    def get_graph_data(self, graph_type, start_date, end_date):
        """Get graph data with validation"""
        try:
            self._validate_session()
            
            if not all([graph_type, start_date, end_date]):
                raise ValueError("Missing required parameters")

            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except:
                pass
                
            if start_date > end_date:
                raise ValueError("Start date must be before end date")

            logger.info(f"Fetching {graph_type} data from {start_date} to {end_date}")

            query = None
            if graph_type == "Gelir Analizi":
                # Revenue analysis by payment provider
                query = self.db_session.query(
                    PaymentDetails.provider,
                    func.sum(PaymentDetails.amount).label('total_revenue'),
                    func.count(PaymentDetails.payment_id).label('transaction_count')
                ).filter(
                    PaymentDetails.created_at.between(start_date, end_date)
                ).group_by(PaymentDetails.provider)

            elif graph_type == "Ürün Satışları":
                # Top 10 products by sales revenue
                query = self.db_session.query(
                    Product.product_name,
                    func.sum(OrderItems.quantity).label('units_sold'),
                    func.sum(Product.price * OrderItems.quantity).label('revenue')
                ).join(
                    OrderItems
                ).filter(
                    Product.created_at.between(start_date, end_date)
                ).group_by(
                    Product.product_name
                ).order_by(
                    func.sum(Product.price * OrderItems.quantity).desc()
                ).limit(10)
                
            elif graph_type == "Müşteri Aktivitesi":
                # Customer shopping session analysis - Top 10 cities
                query = self.db_session.query(
                    CustomerAddress.city,
                    func.count(ShoppingSession.session_id).label('session_count'),
                    func.avg(ShoppingSession.total).label('avg_cart_value')
                ).select_from(CustomerAddress).join(
                    ShoppingSession, 
                    CustomerAddress.customer_id == ShoppingSession.customer_id
                ).filter(
                    ShoppingSession.created_at.between(start_date, end_date)
                ).group_by(
                    CustomerAddress.city
                ).order_by(
                    func.count(ShoppingSession.session_id).desc()
                ).limit(10)

            elif graph_type == "Sipariş Durumu":
                # Order status distribution
                query = self.db_session.query(
                    OrderDetails.order_status,
                    func.count(OrderDetails.order_id).label('order_count'),
                    func.sum(OrderDetails.total).label('total_value')
                ).filter(
                    OrderDetails.created_at.between(start_date, end_date)
                ).group_by(OrderDetails.order_status)

            elif graph_type == "Kategori Performansı":
                # Category performance with discount impact
                query = self.db_session.query(
                    Category.category_name,
                    func.count(Product.product_id).label('product_count'),
                    func.avg(Discount.discount_percentage).label('avg_discount'),
                    func.sum(OrderItems.quantity).label('total_sold')
                ).select_from(Category).join(
                    Product,
                    Category.category_id == Product.category_id
                ).join(
                    OrderItems,
                    Product.product_id == OrderItems.product_id
                ).outerjoin(
                    Discount,
                    Product.discount_id == Discount.discount_id
                ).filter(
                    Product.created_at.between(start_date, end_date)
                ).group_by(Category.category_name)

            if query is None:
                raise ValueError(f"Invalid graph type: {graph_type}")

            result = query.all()
            if not result:
                logger.warning(f"No data found for {graph_type} between {start_date} and {end_date}")
                return []

            logger.info(f"Found {len(result)} records")
            return [row._asdict() for row in result]

        except Exception as e:
            logger.error(f"Error fetching graph data: {str(e)}")
            if self.db_session:
                self.db_session.rollback()
            raise

        finally:
            if self.db_session:
                self.db_session.close()