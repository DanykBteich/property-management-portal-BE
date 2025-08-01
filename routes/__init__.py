from flask import Blueprint
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy.orm import Query as BaseQuery
from dotenv import load_dotenv
import os

from .properties import bp as properties_bp
from .tenants import bp as tenants_bp
from .tasks import bp as tasks_bp

load_dotenv()
version_number = os.getenv("VERSION_NUMBER", "v1")

api_bp = Blueprint("api", __name__, url_prefix=f"/api/{version_number}")

api_bp.register_blueprint(properties_bp)
api_bp.register_blueprint(tenants_bp)
api_bp.register_blueprint(tasks_bp)

# Centralized error handlers
@api_bp.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"Error": str(e)}), 400

@api_bp.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({"Error": "Not Found"}), 404