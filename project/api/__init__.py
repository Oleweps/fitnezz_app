from flask import Blueprint
#api flask blueprint

bp = Blueprint('api', __name__)
from project.api import routes