"""
    Shared types validators schemas
"""
from marshmallow import validate

PROPERTY_TYPE = validate.OneOf([
    "Residential",
    "Commercial"
])