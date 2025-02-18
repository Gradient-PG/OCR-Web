import os

from flask import Flask, session, render_template, jsonify
from flask_session import Session
from datetime import timedelta
from app.core.db import get_db
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS
from flask_talisman import Talisman
from flask_mail import Mail

app = Flask(
    __name__,
    static_folder="dist/static", # vol/static for production
    template_folder="dist",
    static_url_path="/static",
)
db = get_db()
app.config["SESSION_TYPE"] = "mongodb"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "SECRET")
app.config["SESSION_PERMANENT"] = True  # bo czas ustawiamy
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1)
app.config["SESSION_MONGODB"] = db.client
app.config["SESSION_MONGODB_DB"] = db.name
app.config["SESSION_MONGODB_COLLECT"] = "sessions"
app.config.from_object(__name__)
Session(app)

csrf = CSRFProtect(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:80"}})
talisman = Talisman(
    app,
    force_https=False,
    x_content_type_options='nosniff',
    content_security_policy={ # change to https later
        'default-src': ["'self'", 'strict-dynamic'],
        'script-src': ["'self'", 'http://localhost:80'],
        'style-src': ["'self'", 'http://localhost:80'],
        'img-src': ["'self'", 'data:', 'http://localhost:80'],
        'connect-src': ["'self'", 'http://localhost:80'],
        'frame-ancestors': ["'none'"],
        'form-action': ["'self'", 'http://localhost:80'],
    },
    strict_transport_security=True,
    frame_options='DENY',
    x_xss_protection='1; mode=block',
    referrer_policy='strict-origin-when-cross-origin'
)

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '9f4526651cc32c'
app.config['MAIL_PASSWORD'] = '2584c6d43448b7'
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@demomailtrap.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

from app.admin.views import admin_bp
from app.card.views import card_bp
from app.auth.views import auth_bp
from app.image.views import image_bp
from app.agreement.views import agreement_bp
from app.retraining.views import retraining_bp

csrf.exempt(retraining_bp)
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(card_bp, url_prefix="/api/card")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(image_bp, url_prefix="/api/image")
app.register_blueprint(retraining_bp, url_prefix="/api/retraining")
app.register_blueprint(agreement_bp, url_prefix="/api/agreement")

@app.route("/api/csrf-token", methods=["GET"])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")


@app.after_request
def add_csrf_cookie(response):
    if response.status_code in range(200, 400) and not response.direct_passthrough:
        response.set_cookie("csrftoken", generate_csrf(), secure=True, samesite="Lax")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
