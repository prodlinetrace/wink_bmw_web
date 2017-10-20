from flask import Blueprint

programs = Blueprint('programs', __name__)

from . import routes
