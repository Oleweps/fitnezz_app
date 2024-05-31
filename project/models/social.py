from project.extensions import db
from project.models.basemodel import BaseModel

class Social(BaseModel):
    __tablename__ = "social"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(100), nullable=False) # e.g., 'pending', 'accepted'
