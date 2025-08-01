from .base import db

class PropertyModel(db.Model):
    __tablename__ = "properties"
    PropId = db.Column(db.Integer, primary_key=True)
    PropAddress = db.Column(db.String, nullable=False)
    PropType = db.Column(db.String, nullable=False)
    PropStatus = db.Column(db.String, nullable=False)
    PropPurchaseDate = db.Column(db.Date, nullable=False)
    PropPrice = db.Column(db.Integer, nullable=False)
    
    tenants = db.relationship("TenantModel", back_populates="property", cascade="all, delete-orphan")
    tasks = db.relationship("TaskModel", back_populates="property", cascade="all, delete-orphan")