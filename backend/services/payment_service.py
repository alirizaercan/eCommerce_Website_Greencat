# backend/services/payment_service.py
from models.payment_details import PaymentDetails
from sqlalchemy.orm import Session
from services.base_service import BaseService
import random

class PaymentService(BaseService):
    STATUSES = ["Success", "Pending", "Failed"]
    
    def __init__(self, session):
        super().__init__(session)
        self.db_session = session
    
    @staticmethod
    def determine_card_type(card_number: str) -> str:
        last_digit = int(card_number[-1])  # Kart numarasının son hanesi
        if 0 <= last_digit <= 3:
            return 'VISA'
        elif 4 <= last_digit <= 6:
            return 'MASTERCARD'
        elif 7 <= last_digit <= 9:
            return 'TROY'
        return 'UNKNOWN'


    def create_payment(self, order_id: int, amount: float, tax: float, provider: str, status: str):
            payment = PaymentDetails(order_id=order_id, amount=amount, tax=tax, provider=provider, status=status)
            self.db_session.add(payment)
            self.db_session.commit()
            return payment
    
    def process_payment(self, payment_data: dict):
        try:
            if not payment_data.get('order_id'):
                raise ValueError("Order ID is required")
                
            payment = PaymentDetails(
                order_id=payment_data['order_id'],
                amount=float(payment_data['amount']),
                tax=float(payment_data['amount']) * 0.18,
                provider=payment_data.get('card_type', 'UNKNOWN'),
                status='PENDING'
            )
            
            self.db_session.add(payment)
            self.db_session.flush()
            
            # Validate card info without storing
            if self._validate_card_details(payment_data):
                payment.status = 'Success'
                self.db_session.commit()
                return {
                    'success': True,
                    'payment_id': payment.payment_id
                }
                
            raise ValueError("Invalid card details")
            
        except Exception as e:
            self.db_session.rollback()
            raise

    def _validate_card_details(self, data):
        # Validate without storing sensitive data
        required = ['card_number', 'card_holder', 'expiry_date', 'cvv']
        return all(data.get(field) for field in required)

    def get_all_payments(self):
        return self.db_session.query(PaymentDetails).all()

    def get_payment_by_id(self, payment_id: int):
        return self.db_session.query(PaymentDetails).filter(PaymentDetails.payment_id == payment_id).first()

    def update_payment(self, payment_id: int, amount: float, tax: float, provider: str, status: str):
        payment = self.db_session.query(PaymentDetails).filter(PaymentDetails.payment_id == payment_id).first()
        if payment:
            payment.amount = amount
            payment.tax = tax
            payment.provider = provider
            payment.status = status
            self.db_session.commit()
        return payment

    def delete_payment(self, payment_id: int):
        payment = self.db_session.query(PaymentDetails).filter(PaymentDetails.payment_id == payment_id).first()
        if payment:
            self.db_session.delete(payment)
            self.db_session.commit()
        return payment