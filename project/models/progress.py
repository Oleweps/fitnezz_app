from project.extensions import db
from project.models.basemodel import BaseModel

class Progress(BaseModel):
    __tablename__ = "progress"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=True) # User's weight
    body_fat_percentage = db.Column(db.Float, nullable=True) # Body fat percentage
