"""
    Endpoints for Properties
"""
import os
from flask import Blueprint, request, jsonify
from models import db, PropertyModel
from schemas import PropertySchema, PropertyCreateSchema
from .utils import paginate_query
from flasgger import swag_from

bp = Blueprint("properties", __name__, url_prefix="/properties")

property_schema = PropertySchema()
property_create_schema = PropertyCreateSchema()
properties_schema = PropertySchema(many=True)

SPEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "specs", "properties"))

@bp.route("/", methods=["GET"])
@swag_from(os.path.join(SPEC_DIR, "prop_list.yaml"), methods=['GET'])
def Get_list_properties():
    query = PropertyModel.query.order_by(PropertyModel.PropId)
    result = paginate_query(query, properties_schema)
    return jsonify(result)

@bp.route("/", methods=["POST"])
@swag_from(os.path.join(SPEC_DIR, "prop_create.yaml"), methods=['POST'])
def Create_property():
    data = request.get_json(force=True)
    prop = property_create_schema.load(data)
    db.session.add(prop)
    db.session.commit()
    return jsonify(property_create_schema.dump(prop)), 201

@bp.route("/<int:PropId>", methods=["GET"])
@swag_from(os.path.join(SPEC_DIR, "prop_get.yaml"), methods=['GET'])
def Get_property(PropId):
    prop = db.session.get(PropertyModel, PropId)
    if prop is None:
        return jsonify({"Message": f"Property id {PropId} not found"}), 404
        
    return jsonify(property_schema.dump(prop))

@bp.route("/<int:PropId>", methods=["PUT"])
@swag_from(os.path.join(SPEC_DIR, "prop_update.yaml"), methods=['PUT'])
def Update_property(PropId):
    prop = db.session.get(PropertyModel, PropId)
    if prop is None:
        return jsonify({"Message": f"Property id {PropId} not found"}), 404
        
    data = request.get_json(force=True)
    for key, value in data.items():
        setattr(prop, key, value)
    db.session.commit()
    return jsonify(property_create_schema.dump(prop)), 200

@bp.route("/<int:PropId>", methods=["DELETE"])
@swag_from(os.path.join(SPEC_DIR, "prop_delete.yaml"), methods=['DELETE'])
def Delete_property(PropId):
    prop = db.session.get(PropertyModel, PropId)
    if prop is None:
        return jsonify({"Message": f"Property id {PropId} not found"}), 404
        
    db.session.delete(prop)
    db.session.commit()
    return jsonify({"Message": f"Property id {PropId} deleted successfully"}), 204
