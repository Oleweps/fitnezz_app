from flask_login import UserMixin
from project.extensions import db
from project.models.basemodel import BaseModel

class User(UserMixin, BaseModel):
    __tablename__ = "users"
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)

    # Relationships
    goals = db.relationship('Goal', backref='user', lazy=True)
    workouts = db.relationship('Workout', backref='user', lazy=True)
    progress = db.relationship('Progress', backref='user', lazy=True)
    nutrition = db.relationship('Nutrition', backref='user', lazy=True)
    social = db.relationship('Social', foreign_keys='Social.user_id', backref='user', lazy=True, primaryjoin="User.id==Social.user_id")
    friends = db.relationship('Social', foreign_keys='Social.friend_id', backref='friend', lazy=True, primaryjoin="User.id==Social.friend_id")
