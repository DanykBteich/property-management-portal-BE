"""
    Endpoints for to manage the entry points of the application
"""
from flask import Blueprint, jsonify
from dotenv import load_dotenv
import os

bp = Blueprint("entry", __name__)
load_dotenv()
version_number = os.getenv("VERSION_NUMBER", "v1")

@bp.route("/", methods=["GET"])
def root_entry():
    return jsonify({
        "message": "Welcome to the Properties Management API",
        "API Base": f"/api/{version_number}",
        "Endpoints": [
            f"/api/{version_number}/properties",
            f"/api/{version_number}/tenants",
            f"/api/{version_number}/tasks"
        ]
    })
    
@bp.route(f"/api/{version_number}/", methods=["GET"])
def api_root_entry():
    return jsonify({
        "message": "Welcome to the Properties Management API",
        "Endpoints": [
            f"/api/{version_number}/properties",
            f"/api/{version_number}/tenants",
            f"/api/{version_number}/tasks"
        ]
    })