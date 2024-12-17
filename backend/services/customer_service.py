# backend/services/customer_service.py
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from models.customer import Customer
from utils.database import Database

db_session = Database().connect()

def register_customer(first_name, last_name, username, email, password, phone_number):
    """
    Registers a new customer.
    Returns the created customer or None if username/email/phone_number is already taken.
    """
    hashed_password = generate_password_hash(password)
    new_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=hashed_password,
        phone_number=phone_number
    )

    try:
        db_session.add(new_customer)
        db_session.commit()
        return new_customer
    except IntegrityError:
        db_session.rollback()
        return None

def login_customer(username, password):
    """
    Logs in a customer by verifying the username and password.
    Returns the customer object if successful, None otherwise.
    """
    customer = db_session.query(Customer).filter(Customer.username == username).first()
    if customer and check_password_hash(customer.password, password):
        customer.login_attempts += 1
        db_session.commit()
        return customer
    elif customer:
        customer.wrong_login_attempts += 1
        db_session.commit()
    return None

def get_customer_by_id(customer_id):
    """
    Fetches a customer by their ID.
    Returns the customer object or None if not found.
    """
    return db_session.query(Customer).filter(Customer.customer_id == customer_id).first()

def update_customer(customer_id, **kwargs):
    """
    Updates customer details.
    Accepts keyword arguments for fields to update.
    Returns the updated customer object or None if not found.
    """
    customer = get_customer_by_id(customer_id)
    if not customer:
        return None

    for key, value in kwargs.items():
        if hasattr(customer, key):
            setattr(customer, key, value)

    db_session.commit()
    return customer

def delete_customer(customer_id):
    """
    Deletes a customer by their ID.
    Returns True if successful, False otherwise.
    """
    customer = get_customer_by_id(customer_id)
    if not customer:
        return False

    db_session.delete(customer)
    db_session.commit()
    return True