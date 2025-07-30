"""
    Contains all the schemas needed
"""
from marshmallow import Schema, fields, validate, post_load
from models import Property, Tenant, Task

property_status = validate.OneOf([
    "Vacant",
    "Occupied"
])

property_type = validate.OneOf([
    "Residential",
    "Commercial"
])

tenant_status = validate.OneOf([
    "Paid",
    "Pending"
])

task_status = validate.OneOf([
    "Completed",
    "In Progress",
    "Pending"
])

class PropertySchema(Schema):
    PropId = fields.Int(dump_only=True)
    PropAddress = fields.Str(required=True)
    PropType = fields.Str(required=True, validate=property_type)
    PropStatus = fields.Str(required=True, validate=property_status)
    PropPurchaseDate = fields.Date(required=True)
    PropPrice = fields.Int(required=True)
    
    @post_load
    def make_task(self, data, **kwargs):
        return Property(**data)
    
class TenantSchema(Schema):
    TenantId = fields.Int(dump_only=True)
    TenantName = fields.Str(required=True)
    TenantContactInfo = fields.Str(required=True)
    TenantLeaseTermStart = fields.Date(required=True)
    TenantLeaseTermEnd = fields.Date(required=True)
    TenantRentalPaymentStatus = fields.Str(required=True, validate=tenant_status)
    PropId = fields.Int(required=True)
    
    @post_load
    def make_task(self, data, **kwargs):
        return Tenant(**data)
    
class TaskSchema(Schema):
    TaskId = fields.Int(dump_only=True)
    TaskDescription = fields.Str(required=True)
    TaskStatus = fields.Str(required=True, validate=task_status)
    TaskScheduledDate = fields.Date(required=True)
    PropId = fields.Int(required=True)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)