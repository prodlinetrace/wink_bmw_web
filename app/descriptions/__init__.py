from flask import Blueprint

descriptions = Blueprint('descriptions', __name__)

from . import routes
