from flask import request, jsonify, Blueprint

from app.card.model import load_cards
from app.image.model import load_images

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/upload-data', methods=['POST'])
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    if not isinstance(data, list):
        return jsonify({"error": "Invalid data type"}), 400

    try:
        response, status_code = load_cards(data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500

@admin_bp.route('/upload-images', methods=['POST'])
def upload_image():
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files provided"}), 400

    try:
        response, status_code = load_images(files)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500