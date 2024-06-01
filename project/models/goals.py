from project.extensions import db
from project.models.basemodel import BaseModel

class Goal(BaseModel):
    __tablename__ = "goals"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    target_date = db.Column(db.Date, nullable=False)


