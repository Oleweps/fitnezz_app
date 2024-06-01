from flask import Blueprint
#blueprints for the feature

bp = Blueprint('feature', __name__)
from project.feature import routes