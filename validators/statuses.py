"""
    Shared status validators schemas
"""
from marshmallow import validate

PROPERTY_STATUS = validate.OneOf([
    "Vacant",
    "Occupied"
])

TENANT_STATUS = validate.OneOf([
    "Paid",
    "Pending"
])

TASK_STATUS = validate.OneOf([
    "Completed",
    "In Progress",
    "Pending"
])