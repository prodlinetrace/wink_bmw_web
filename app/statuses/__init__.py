from flask import Blueprint

statuses = Blueprint('statuses', __name__)

from . import routes
