from flask import Blueprint

stations = Blueprint('stations', __name__)

from . import routes
