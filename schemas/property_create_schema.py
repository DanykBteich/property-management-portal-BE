from marshmallow import Schema, fields, post_load
from models import PropertyModel
from validators.statuses import PROPERTY_STATUS
from validators.types import PROPERTY_TYPE

class PropertyCreateSchema(Schema):
    PropAddress = fields.Str(required=True)
    PropType = fields.Str(required=True, validate=PROPERTY_TYPE)
    PropStatus = fields.Str(required=True, validate=PROPERTY_STATUS)
    PropPurchaseDate = fields.Date(required=True)
    PropPrice = fields.Int(required=True)
    
    @post_load
    def make_property(self, data, **kwargs):
        """
            Create a Property instance from the deserialized data
        """
        return PropertyModel(**data)