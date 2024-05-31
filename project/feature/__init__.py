from flask import Blueprint

bp = Blueprint('feature', __name__)
from project.feature import routes