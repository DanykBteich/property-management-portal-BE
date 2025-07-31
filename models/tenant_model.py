from .base import db

class TenantModel(db.Model):
    __tablename__ = "tenants"
    TenantId = db.Column(db.Integer, primary_key=True)
    TenantName = db.Column(db.String, nullable=False)
    TenantContactInfo = db.Column(db.String, nullable=False)
    TenantLeaseTermStart = db.Column(db.Date, nullable=False)
    TenantLeaseTermEnd = db.Column(db.Date, nullable=False)
    TenantRentalPaymentStatus = db.Column(db.String, nullable=False)
    
    PropId = db.Column(db.Integer, db.ForeignKey("properties.PropId"), nullable=False)
    property = db.relationship("PropertyModel", back_populates="tenants")