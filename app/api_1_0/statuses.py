from flask import jsonify, g
from .. import db
from ..models import Status

from . import webapi
from .errors import forbidden, bad_request
from flask.ext.babel import gettext

@webapi.route('/statuses/<int:id>', methods=['DELETE'])
def delete_status(id):
    status = Status.query.get_or_404(id)
    if not g.current_user.is_admin:
        return forbidden(gettext('You cannot modify this status.'))
    db.session.delete(status)
    db.session.commit()
    return jsonify({'status': 'ok'})
