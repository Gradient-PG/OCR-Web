from flask import request, jsonify, Blueprint
from app.card.model import (load_cards, find_card_by_image_code, delete_card_by_image_code,
                            retrieve_all_image_codes_from_cards)
from app.image.model import load_images
from app.admin.model import create_user, user_exists
from app.auth.decorators import admin_required
from app.core.utils import parse_json
from app.card.model import (get_card_by_id, update_card, increment_correct)

admin_bp = Blueprint('admin', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@admin_bp.route('/upload-data', methods=['POST'])
@admin_required
def upload_data():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "No JSON data provided"}), 400

    if not isinstance(data, list):
        return jsonify({"error": "Invalid data type"}), 400

    try:
        response, status_code = load_cards(data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500


@admin_bp.route('/upload-images', methods=['POST'])
@admin_required
def upload_image():
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files provided"}), 400

    try:
        response, status_code = load_images(files)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500


@admin_bp.route('/add-user', methods=['POST'])
@admin_required
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON data provided"}), 400
    try:
        if user_exists(data):
            return jsonify({"message": "user with this login already exists"}), 400

        password = create_user(data)
        return {"message": f"user added sucessfully!"}, 200
    except Exception as e:
        return jsonify({"message": f"Failed to add user: {str(e)}"}), 500




@admin_bp.route('/cards', methods=['GET'])
@admin_required
def get_all_cards():
    return retrieve_all_image_codes_from_cards()


@admin_bp.route('/card/<image_code>', methods=['DELETE'])
@admin_required
def delete_card(image_code):
    response, status  = delete_card_by_image_code(image_code)
    return response, status


@admin_bp.route('/card/<image_code>', methods=['GET'])
@admin_required
def get_card(image_code):
    # to get image -> go to image blueprint
    card = find_card_by_image_code(image_code)
    parsed_card = parse_json(card)
    if not parsed_card:
        return jsonify({"error": "No cards available in the database."}), 400

    return jsonify(parsed_card)

@admin_bp.route('/correct', methods=["POST"])
@admin_required
def receive_correct_card():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    card_id = data.get('_id')
    if not card_id:
        return jsonify({"error": "No card ID provided"}), 400

    card = get_card_by_id(card_id)
    if not card:
        return jsonify({"error": "Card not found"}), 404

    data.pop("correct", None)
    data.pop("_id", None)
    data.pop("checked_by", None)

    if update_card(card_id, data):
        increment_correct(card_id, 'admin', 3)
        return jsonify({"message": "Card marked as correct and updated."}), 200
    else:
        return jsonify({"error": "Error updating card."}), 500


# TEMPORARY FOR TESTING, WILL BE DELETED IN PROD VERSION
from app.core.db import get_db
import bcrypt
@admin_bp.route('/temp-admin', methods=['POST'])
def create_temp_admin():
    db = get_db()
    collection = db['users']

    data = request.get_json()

    password = 'admin'
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    data['login'] = 'admin'
    data['password'] = hashed_password
    data['is_super_user'] = True

    collection.insert_one(data)
    return {"message": f"Admin created! Login: admin Password: admin"}, 200

