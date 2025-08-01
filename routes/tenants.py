"""
    Endpoints for Tenants
"""
import os
from flask import Blueprint, request, jsonify
from models import db, TenantModel
from schemas import TenantSchema, TenantCreateSchema
from .utils import paginate_query
from flasgger import swag_from

bp = Blueprint("tenants", __name__, url_prefix="/tenants")

tenant_schema = TenantSchema()
tenant_create_schema = TenantCreateSchema()
tenants_schema = TenantSchema(many=True)

SPEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "specs", "tenants"))

@bp.route("/", methods=["GET"])
@swag_from(os.path.join(SPEC_DIR, "tenants_list.yaml"), methods=["GET"])
def Get_list_tenants():
    query = TenantModel.query.order_by(TenantModel.TenantId)
    result = paginate_query(query, tenants_schema)
    return jsonify(result)

@bp.route("/", methods=["POST"])
@swag_from(os.path.join(SPEC_DIR, "tenants_create.yaml"), methods=["POST"])
def Create_tenant():
    data = request.get_json(force=True)
    tenant = tenant_create_schema.load(data)
    db.session.add(tenant)
    db.session.commit()
    return jsonify(tenant_create_schema.dump(tenant)), 201

@bp.route("/<int:TenantId>", methods=["GET"])
@swag_from(os.path.join(SPEC_DIR, "tenants_get.yaml"), methods=["GET"])
def Get_tenant(TenantId):
    tenant = db.session.get(TenantModel, TenantId)
    if tenant is None:
        return jsonify({"Message": f"Tenant id {TenantId} not found"}), 404
    
    return jsonify(tenant_schema.dump(tenant))

@bp.route("/<int:TenantId>", methods=["PUT"])
@swag_from(os.path.join(SPEC_DIR, "tenants_update.yaml"), methods=["PUT"])
def Update_tenant(TenantId):
    tenant = db.session.get(TenantModel, TenantId)
    if tenant is None:
        return jsonify({"Message": f"Tenant id {TenantId} not found"}), 404
    
    data = request.get_json(force=True)
    for key, value in data.items():
        setattr(tenant, key, value)
    db.session.commit()
    return jsonify(tenant_schema.dump(tenant))

@bp.route("/<int:TenantId>", methods=["DELETE"])
@swag_from(os.path.join(SPEC_DIR, "tenants_delete.yaml"), methods=["DELETE"])
def Delete_tenant(TenantId):
    tenant = db.session.get(TenantModel, TenantId)
    if tenant is None:
        return jsonify({"Message": f"Tenant id {TenantId} not found"}), 404
    
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({"Message": f"Tenant id {TenantId} deleted successfully"}), 204
