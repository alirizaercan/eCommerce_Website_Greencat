# backend/controllers/inventory_controller.py
from flask import Blueprint, request, jsonify
from utils.database import Database
from services.inventory_service import InventoryService

inventory_controller = Blueprint('inventory_controller', __name__)
db = Database()

@inventory_controller.route('/inventories', methods=['POST'])
def create_inventory():
    data = request.get_json()
    inventory_service = InventoryService(db.session)
    inventory = inventory_service.create_inventory(data['quantity'])
    return jsonify(inventory), 201

@inventory_controller.route('/inventories', methods=['GET'])
def get_all_inventories():
    inventory_service = InventoryService(db.session)
    inventories = inventory_service.get_all_inventories()
    return jsonify(inventories), 200

@inventory_controller.route('/inventories/<int:inventory_id>', methods=['GET'])
def get_inventory_by_id(inventory_id):
    inventory_service = InventoryService(db.session)
    inventory = inventory_service.get_inventory_by_id(inventory_id)
    if inventory:
        return jsonify(inventory), 200
    return jsonify({'message': 'Inventory not found'}), 404

@inventory_controller.route('/inventories/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    data = request.get_json()
    inventory_service = InventoryService(db.session)
    inventory = inventory_service.update_inventory(inventory_id, data['quantity'])
    if inventory:
        return jsonify(inventory), 200
    return jsonify({'message': 'Inventory not found'}), 404

@inventory_controller.route('/inventories/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    inventory_service = InventoryService(db.session)
    inventory = inventory_service.delete_inventory(inventory_id)
    if inventory:
        return jsonify({'message': 'Inventory deleted'}), 200
    return jsonify({'message': 'Inventory not found'}), 404