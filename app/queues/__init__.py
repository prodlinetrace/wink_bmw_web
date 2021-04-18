from flask import Blueprint

queues = Blueprint('queues', __name__)

from . import routes
