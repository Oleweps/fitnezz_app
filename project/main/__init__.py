from flask import Blueprint
#main flask route blueprint ceation
bp = Blueprint('main', __name__)
from project.main import routes