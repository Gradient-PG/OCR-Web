import sys
sys.path.insert(0, '..')
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app.card.views import card_bp
from app.admin.views import admin_bp


def mock_getenv_side_effect(key, default=None):
    return {
        "MONGO_HOST": "localhost",
        "MONGO_PORT": "27017",
        "MONGO_USER": "root",
        "MONGO_PASS": "pass",
    }.get(key, default)


class TestCardRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(card_bp)
        self.app.register_blueprint(admin_bp)
        self.client = self.app.test_client()

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_upload__card_data(self, mock_getenv, mock_mongo_client):
        personal_card_data = {
            "name": "John",
            "surname": "Doe21",
        }
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db['cards'] = mock_collection
        mock_mongo_client.return_value = mock_db

        response = self.client.post(
            "/upload-data",
            data=json.dumps(personal_card_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Card successfully uploaded.", response.json["message"])

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_upload_card_data_invalid_json(self, mock_getenv, mock_mongo_client):
        invalid_json = '{"name": "John", "surname": "Doe"'

        response = self.client.post(
            "/upload-data",
            data=invalid_json,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_correct_card_success(self, mock_getenv, mock_mongo_client):
        correct_card_data = {"_id": "123", "name": "John", "surname": "Doe"}

        response = self.client.post(
            "/correct-card",
            data=json.dumps(correct_card_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Card marked as correct and updated.", response.json["message"])

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_random_card_no_incorrect_cards(self, mock_getenv, mock_mongo_client):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db['cards'] = mock_collection
        mock_mongo_client.return_value = mock_db
        mock_collection.find.return_value = []

        response = self.client.get("/random-card")

        self.assertEqual(response.status_code, 400)
        self.assertIn("No cards available in the database.", response.json["error"])

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_upload_get_correct_random_card(self, mock_getenv, mock_mongo_client):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db['cards'] = mock_collection
        mock_mongo_client.return_value = mock_db
        mock_collection.find.return_value = []

        card_data = {
            "name": "John",
            "surname": "Doe21",
            "correct": False
        }
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db['cards'] = mock_collection
        mock_mongo_client.return_value = mock_db

        # Step 1: Upload the card
        response = self.client.post(
            "/upload-data",
            data=json.dumps(card_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Card successfully uploaded.", response.json["message"])

        # correct card
        correct_card_data = {"_id": "1", "name": "John", "surname": "Doe21"}

        response = self.client.post(
            "/correct-card",
            data=json.dumps(correct_card_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Card marked as correct and updated.", response.json["message"])


if __name__ == "__main__":
    unittest.main()
