import os
from flask import Flask
from models import db
from models.ingestion import ingest_data
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    
    db.init_app(app)
    
    with app.app_context():
        ingest_data()
        
    return app