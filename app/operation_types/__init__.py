from flask import Blueprint

operation_types = Blueprint('operation_types', __name__)

from . import routes
