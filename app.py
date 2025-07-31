import os
from flask import Flask
from models import db
from models.ingestion import ingest_data
from dotenv import load_dotenv
from routes import api_bp
from routes.entry import bp as entry_bp

def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    
    db.init_app(app)
    
    with app.app_context():
        ingest_data()
        app.register_blueprint(entry_bp)
        app.register_blueprint(api_bp)
    
    return app