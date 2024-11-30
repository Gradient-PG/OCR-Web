from flask import jsonify, request, Blueprint
from app.core.utils import parse_json
from .model import get_image

image_bp = Blueprint('image', __name__)

@image_bp.route('/image/<image_code>', methods=['GET'])
def send_photo(image_code):
    try:
        image_data = get_image(image_code)
        if not image_data:
            return jsonify({"error": "No such a card in db"}), 400
        image_data = parse_json(image_data)
        return jsonify(image_data), 200
    except Exception as e:
         print(f"An error occurred: {e}")
         return jsonify({"error": f"An error occurred: {str(e)}"}), 500
