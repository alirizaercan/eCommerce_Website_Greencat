# backend/services/discount_service.py
from models.discount import Discount
from sqlalchemy.orm import Session

class DiscountService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_discount(self, discount_name: str, discount_description: str, discount_percentage: float, active: bool = True):
        discount = Discount(discount_name=discount_name, discount_description=discount_description, discount_percentage=discount_percentage, active=active)
        self.db_session.add(discount)
        self.db_session.commit()
        return discount

    def get_all_discounts(self):
        return self.db_session.query(Discount).all()

    def get_discount_by_id(self, discount_id: int):
        return self.db_session.query(Discount).filter(Discount.discount_id == discount_id).first()

    def update_discount(self, discount_id: int, discount_name: str, discount_description: str, discount_percentage: float, active: bool):
        discount = self.db_session.query(Discount).filter(Discount.discount_id == discount_id).first()
        if discount:
            discount.discount_name = discount_name
            discount.discount_description = discount_description
            discount.discount_percentage = discount_percentage
            discount.active = active
            self.db_session.commit()
        return discount

    def delete_discount(self, discount_id: int):
        discount = self.db_session.query(Discount).filter(Discount.discount_id == discount_id).first()
        if discount:
            self.db_session.delete(discount)
            self.db_session.commit()
        return discount