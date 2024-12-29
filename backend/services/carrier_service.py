# backend/services/carrier_service.py
from models.carrier import Carrier
from sqlalchemy.orm import Session
import random

class CarrierService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    CARRIERS = [
        "FedEx",
        "DHL",
        "UPS",
        "Yurtiçi Kargo",
        "Aras Kargo",
        "MNG Kargo",
        "PTT Kargo"
    ]

    @staticmethod
    def assign_random_carrier():
        return random.choice(CarrierService.CARRIERS)

    def create_carrier(self, carrier_name: str, carrier_phone: str, carrier_email: str):
        carrier = Carrier(carrier_name=carrier_name, carrier_phone=carrier_phone, carrier_email=carrier_email)
        self.db_session.add(carrier)
        self.db_session.commit()
        return carrier

    def get_all_carriers(self):
        return self.db_session.query(Carrier).all()

    def get_carrier_by_id(self, carrier_id: int):
        return self.db_session.query(Carrier).filter(Carrier.carrier_id == carrier_id).first()

    def update_carrier(self, carrier_id: int, carrier_name: str, carrier_phone: str, carrier_email: str):
        carrier = self.db_session.query(Carrier).filter(Carrier.carrier_id == carrier_id).first()
        if carrier:
            carrier.carrier_name = carrier_name
            carrier.carrier_phone = carrier_phone
            carrier.carrier_email = carrier_email
            self.db_session.commit()
        return carrier

    def delete_carrier(self, carrier_id: int):
        carrier = self.db_session.query(Carrier).filter(Carrier.carrier_id == carrier_id).first()
        if carrier:
            self.db_session.delete(carrier)
            self.db_session.commit()
        return carrier