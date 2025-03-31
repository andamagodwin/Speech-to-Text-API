from flask import Flask
from .routes import bp
from flask_cors import CORS  # <-- Add this import

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/transcribe": {"origins": "http://localhost:3000"}
    })
    app.register_blueprint(bp)
    return app