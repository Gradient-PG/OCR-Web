import base64
import random
from flask import jsonify, request, Blueprint
from app.core.utils import parse_json
from .model import (get_card_by_id, update_card, increment_correct, get_random_card)
from app.core.db import get_db
from app.core.utils import parse_json

card_bp = Blueprint('card', __name__)

@card_bp.route('/correct-card', methods=['POST'])
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

    if int(card.get("correct", 0)) >= 1:
        card.pop("correct", None)
        card.pop("_id", None)
        if card != data:
            data["correct"] = 0

    if update_card(card_id, data):
        increment_correct(card_id)
        return jsonify({"message": "Card marked as correct and updated."}), 200
    else:
        return jsonify({"error": "Error updating card."}), 500

@card_bp.route('/random-card', methods=['GET'])
def send_random_card():
    card = get_random_card()
    card = parse_json(card)
    if not card:
        return jsonify({"error": "No cards available in the database."}), 400
      
    return jsonify(card), 200
