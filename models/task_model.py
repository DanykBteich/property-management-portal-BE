from .base import db

class TaskModel(db.Model):
    __tablename__ = "tasks"
    TaskId = db.Column(db.Integer, primary_key=True)
    TaskDescription = db.Column(db.String, nullable=False)
    TaskStatus = db.Column(db.String, nullable=False)
    TaskScheduledDate = db.Column(db.Date, nullable=False)
    
    PropId = db.Column(db.Integer, db.ForeignKey("properties.PropId"), nullable=False)
    property = db.relationship("PropertyModel", back_populates="tasks")