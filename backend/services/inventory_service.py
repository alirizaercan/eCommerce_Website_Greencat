# backend/services/inventory_service.py
from models.inventory import Inventory
from sqlalchemy.orm import Session

class InventoryService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_inventory(self, quantity: int):
        inventory = Inventory(quantity=quantity)
        self.db_session.add(inventory)
        self.db_session.commit()
        return inventory

    def get_all_inventories(self):
        return self.db_session.query(Inventory).all()

    def get_inventory_by_id(self, inventory_id: int):
        return self.db_session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()

    def update_inventory(self, inventory_id: int, quantity: int):
        inventory = self.db_session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
        if inventory:
            inventory.quantity = quantity
            self.db_session.commit()
        return inventory

    def delete_inventory(self, inventory_id: int):
        inventory = self.db_session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
        if inventory:
            self.db_session.delete(inventory)
            self.db_session.commit()
        return inventory