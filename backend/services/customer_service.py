# backend/services/customer_service.py
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from models.customer import Customer
from models.customer_adress import CustomerAddress
from services.base_service import BaseService
from utils.database import Database
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CustomerService(BaseService):
    def __init__(self, session=None):
        super().__init__(session)
        self.session = session or self._get_session()   

    def register_customer(self, first_name, last_name, username, email, password, phone_number):
        session = self._get_session()
        try:
            hashed_password = generate_password_hash(password)
            new_customer = Customer(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=hashed_password,
                phone_number=phone_number
            )
            session.add(new_customer)
            session.commit()
            return new_customer
        except IntegrityError:
            session.rollback()
            return None
        finally:
            session.close()

    def login_customer(self, username, password):
        session = self._get_session()
        try:
            customer = session.query(Customer).filter(Customer.username == username).first()
            if customer and check_password_hash(customer.password, password):
                customer.login_attempts += 1
                session.commit()
                # Keep customer bound to session
                session.refresh(customer)
                return customer
            elif customer:
                customer.wrong_login_attempts += 1
                session.commit()
            return None
        except Exception as e:
            session.rollback()
            raise e
            
    def logout_customer(self, customer_id: int) -> bool:
            """Logs out a customer by updating their last_logout timestamp.
            
            Args:
                customer_id: The ID of the customer to logout
                
            Returns:
                bool: True if logout successful, False otherwise
            """
            session = self._get_session()
            try:
                customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
                if customer:
                    customer.last_logout = datetime.utcnow()
                    session.commit()
                    logger.info(f"Customer {customer_id} logged out successfully")
                    return True
                logger.warning(f"Customer {customer_id} not found for logout")
                return False
            except Exception as e:
                logger.error(f"Logout error for customer {customer_id}: {str(e)}")
                session.rollback()
                return False
            finally:
                session.close()

    def get_customer_by_id(self, customer_id):
            try:
                session = self._get_session()
                customer = session.query(Customer)\
                    .filter(Customer.customer_id == customer_id)\
                    .first()
                return customer
            except Exception as e:
                raise Exception(f"Error getting customer: {str(e)}")

    def update_customer(self, customer_id, **kwargs):
        session = self._get_session()
        try:
            customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
            if not customer:
                return None

            for key, value in kwargs.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)

            session.commit()
            return customer
        finally:
            session.close()

    def delete_customer(self, customer_id):
        session = self._get_session()
        try:
            customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
            if not customer:
                return False
            
            session.delete(customer)
            session.commit()
            return True
        finally:
            session.close()

    def create_address(self, customer_id, address_data):
            try:
                new_address = CustomerAddress(**address_data)
                self.session.add(new_address)
                self.session.commit()
                return new_address.to_dict()
            except Exception as e:
                self.session.rollback()
                logger.error(f"Create address error: {str(e)}")
                raise

    # Similarly update other methods to use self.session consistently
    def get_customer_addresses(self, customer_id):
        try:
            addresses = self.session.query(CustomerAddress)\
                .filter(CustomerAddress.customer_id == customer_id)\
                .all()
            return [address.to_dict() for address in addresses]
        except Exception as e:
            logger.error(f"Get addresses error: {str(e)}")
            raise

    def update_address(self, address_id, data):
        try:
            address = self.session.query(CustomerAddress)\
                .filter(CustomerAddress.address_id == address_id)\
                .first()
            if not address:
                return None

            for key, value in data.items():
                if hasattr(address, key):
                    setattr(address, key, value)

            self.session.commit()
            return address
        except Exception as e:
            self.session.rollback()
            logger.error(f"Update address error: {str(e)}")
            raise

    def delete_address(self, address_id):
        try:
            address = self.session.query(CustomerAddress)\
                .filter(CustomerAddress.address_id == address_id)\
                .first()
            if not address:
                return False

            self.session.delete(address)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f"Delete address error: {str(e)}")
            raise

    def add_customer_address(self, customer_id, address_data):
        try:
            new_address = CustomerAddress(
                customer_id=customer_id,
                address_type=address_data.get('addressType'),
                street=address_data.get('street'),
                city=address_data.get('city'),
                state=address_data.get('state'),
                postal_code=address_data.get('postalCode'),
                country=address_data.get('country', 'Turkey')
            )
            self.db_session.add(new_address)
            self.db_session.commit()
            return new_address.to_dict()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_address_by_customer(self, customer_id):
        session = self._get_session()
        try:
            customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
            return customer.addresses if customer else None
        finally:
            session.close()

# Create singleton instance
customer_service = CustomerService()