import os
from flask import Flask
from models import db, ingest_data
from dotenv import load_dotenv
from routes import api_bp
from routes.entry import bp as entry_bp
from flasgger import Swagger
from flask_cors import CORS
import yaml

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    
    # Load Swagger doc from external YAML
    swagger_path = os.path.join(os.path.dirname(__file__), "docs/swagger_template.yaml")
    
    with open(swagger_path) as f:
        swagger_template = yaml.safe_load(f)
    
    app.config.setdefault("SWAGGER", {})  
    app.config["SWAGGER"]["validatorUrl"] = None  

    db.init_app(app)
    
    with app.app_context():
        ingest_data()
        app.register_blueprint(entry_bp)
        app.register_blueprint(api_bp, url_prefix=f"/api/{os.getenv('VERSION_NUMBER', 'v1')}")
    
    Swagger(app, template=swagger_template)
    
    return app