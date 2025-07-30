"""
    Endpoints for Properties
"""
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from models import db, Property
from schemas import PropertySchema
from .utils import paginate_query

bp = Blueprint("properties", __name__, url_prefix="/properties")

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)

@bp.route("/", methods=["GET"])
def Get_list_properties():
    query = Property.query.order_by(Property.PropId)
    result = paginate_query(query, properties_schema)
    return jsonify(result)

@bp.route("/", methods=["POST"])
def Create_property():
    data = request.get_json(force=True)
    prop = property_schema.load(data)
    db.session.add(prop)
    db.session.commit()
    return property_schema.jsonify(prop), 201

@bp.route("/<int:id>", methods=["GET"])
def Get_property(id):
    prop = Property.query.get_or_404(id)
    return property_schema.jsonify(prop)

@bp.route("/<int:id>", methods=["PUT"])
def Update_property(id):
    prop = Property.query.get_or_404(id)
    data = request.get_json(force=True)
    updated_data = property_schema.load(data, instance=prop, partial=True)
    db.session.commit()
    return property_schema.jsonify(updated_data)

@bp.route("/<int:id>", methods=["DELETE"])
def Delete_property(id):
    prop = Property.query.get_or_404(id)
    db.session.delete(prop)
    db.session.commit()
    return jsonify({"Message": f"Property id {id} deleted successfully"}), 204
