# backend/controllers/session_controller.py
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError
from services.session_service import SessionService
from utils.database import Database
import logging

logger = logging.getLogger(__name__)
session_controller = Blueprint('session_controller', __name__)
db = Database()

@session_controller.route('/', methods=['POST', 'OPTIONS'])
@cross_origin()
def create_session():
    if request.method == 'OPTIONS':
        return {'message': 'OK'}, 200

    db_session = db.get_session()
    session_service = SessionService(db_session)
    
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        total = data.get('total', 0)

        if not customer_id:
            return jsonify({"error": "customer_id is required"}), 400

        session = session_service.create_session(customer_id, total)
        return jsonify({"session": session.as_dict()}), 201

    except SQLAlchemyError as e:
        logger.error(f"Database error in create_session: {str(e)}")
        db_session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in create_session: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        db_session.close()

@session_controller.route('/<int:session_id>', methods=['GET', 'OPTIONS'])
def get_session(session_id):
    if request.method == 'OPTIONS':
        return {'message': 'OK'}, 200

    db_session = db.get_session()
    session_service = SessionService(db_session)
    try:
        session = session_service.get_session(session_id)
        if session:
            return jsonify(session)
        return jsonify({"error": "Session not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

@session_controller.route('/<int:session_id>', methods=['PUT', 'OPTIONS'])
def update_session(session_id):
    if request.method == 'OPTIONS':
        return {'message': 'OK'}, 200

    db_session = db.get_session()
    session_service = SessionService(db_session)
    try:
        data = request.get_json()
        total = data.get('total')
        updated_session = session_service.update_session(session_id, total)
        if updated_session:
            return jsonify({"session": updated_session}), 200
        return jsonify({"error": "Session not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

@session_controller.route('/<int:session_id>', methods=['DELETE', 'OPTIONS'])
def delete_session(session_id):
    if request.method == 'OPTIONS':
        return {'message': 'OK'}, 200

    db_session = db.get_session()
    session_service = SessionService(db_session)
    try:
        success = session_service.delete_session(session_id)
        if success:
            return jsonify({"message": "Session deleted successfully"}), 200
        return jsonify({"error": "Session not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()