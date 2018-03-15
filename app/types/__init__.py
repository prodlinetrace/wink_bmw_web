from flask import Blueprint

types = Blueprint('types', __name__)

from . import routes
