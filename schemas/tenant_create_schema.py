from marshmallow import Schema, fields, post_load
from models import TenantModel
from validators.statuses import TENANT_STATUS

class TenantCreateSchema(Schema):
    TenantName = fields.Str(required=True)
    TenantContactInfo = fields.Str(required=True)
    TenantLeaseTermStart = fields.Date(required=True)
    TenantLeaseTermEnd = fields.Date(required=True)
    TenantRentalPaymentStatus = fields.Str(required=True, validate=TENANT_STATUS)
    PropId = fields.Int(required=True)
    
    @post_load
    def make_tenant(self, data, **kwargs):
        """
            Create a Tenant instance from the deserialized data
        """
        return TenantModel(**data)