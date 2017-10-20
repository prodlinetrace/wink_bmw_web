from flask import Blueprint

operation_statuses = Blueprint('operation_statuses', __name__)

from . import routes
