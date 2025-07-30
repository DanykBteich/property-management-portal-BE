import os
from flask import Flask
from flask_migrate import Migrate
from models import db
from models.ingestion import ingest_data
from dotenv import load_dotenv
from routes import api_bp

def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        ingest_data()
        app.register_blueprint(api_bp)
        
    return app