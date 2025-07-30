from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Property(db.Model):
    __tablename__ = "properties"
    PropId = db.Column(db.Integer, primary_key=True)
    PropAddress = db.Column(db.String, nullable=False)
    PropType = db.Column(db.String, nullable=False)
    PropStatus = db.Column(db.String, nullable=False)
    PropPurchaseDate = db.Column(db.Date, nullable=False)
    PropPrice = db.Column(db.Integer, nullable=False)
    
    tenants = db.relationship("Tenant", back_populates="property", cascade="all, delete-orphan")
    tasks = db.relationship("Task", back_populates="property", cascade="all, delete-orphan")

class Tenant(db.Model):
    __tablename__ = "tenants"
    TenantId = db.Column(db.Integer, primary_key=True)
    TenantName = db.Column(db.String, nullable=False)
    TenantContactInfo = db.Column(db.String, nullable=False)
    TenantLeaseTermStart = db.Column(db.Date, nullable=False)
    TenantLeaseTermEnd = db.Column(db.Date, nullable=False)
    TenantRentalPaymentStatus = db.Column(db.String, nullable=False)
    
    PropId = db.Column(db.Integer, db.ForeignKey("properties.PropId"), nullable=False)
    property = db.relationship("Property", back_populates="tenants")

class Task(db.Model):
    __tablename__ = "tasks"
    TaskId = db.Column(db.Integer, primary_key=True)
    TaskDescription = db.Column(db.String, nullable=False)
    TaskStatus = db.Column(db.String, nullable=False)
    TaskScheduledDate = db.Column(db.Date, nullable=False)
    
    PropId = db.Column(db.Integer, db.ForeignKey("properties.PropId"), nullable=False)
    property = db.relationship("Property", back_populates="tasks")