"""
    Endpoints for Tenants
"""
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from models import db, Tenant
from schemas import TenantSchema
from .utils import paginate_query

bp = Blueprint("tenants", __name__, url_prefix="/tenants")

tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)

@bp.route("/", methods=["GET"])
def Get_list_tenants():
    query = Tenant.query.order_by(Tenant.TenantId)
    result = paginate_query(query, tenants_schema)
    return jsonify(result)

@bp.route("/", methods=["POST"])
def Create_tenant():
    data = request.get_json(force=True)
    tenant = tenant_schema.load(data)
    db.session.add(tenant)
    db.session.commit()
    return jsonify(tenant_schema.dump(tenant)), 201

@bp.route("/<int:id>", methods=["GET"])
def Get_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    return tenant_schema.jsonify(tenant)

@bp.route("/<int:id>", methods=["PUT"])
def Update_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    data = request.get_json(force=True)
    for key, value in data.items():
        setattr(tenant, key, value)
    db.session.commit()
    return jsonify(tenant_schema.dump(tenant))

@bp.route("/<int:id>", methods=["DELETE"])
def Delete_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({"Message": f"Tenant id {id} deleted successfully"}), 204
