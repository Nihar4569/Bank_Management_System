# app/__init__.py

from flask import Flask, jsonify
from app.db import init_db, db
from app.config import Config
from app.models import Account
from app.routes import bp as routes_bp   # ✅ Import blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    init_db(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Banking Management System API!"})

    # ✅ Register the routes (this line connects your blueprint)
    app.register_blueprint(routes_bp)

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    return app
