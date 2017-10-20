from flask import jsonify, g
from .. import db
from ..models import Operation

from . import webapi
from .errors import forbidden, bad_request
from flask_babel import gettext

@webapi.route('/operations/<int:id>', methods=['DELETE'])
def delete_operation(id):
    operation = Operation.query.get_or_404(id)
    if not g.current_user.is_admin:
        return forbidden(gettext('You cannot modify this operation.'))
    db.session.delete(operation)
    db.session.commit()
    return jsonify({'status': 'ok'})
