from project.extensions import db
from project.models.basemodel import BaseModel

class Workout(BaseModel):
    __tablename__ = "workouts"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False) # Duration in minutes
