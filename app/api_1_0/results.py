from flask import jsonify, g
from .. import db
from ..models import Result

from . import webapi
from .errors import forbidden, bad_request
from flask_babel import gettext

@webapi.route('/results/<int:id>', methods=['DELETE'])
def delete_result(id):
    result = Result.query.get_or_404(id)
    if not g.current_user.is_admin:
        return forbidden(gettext('You cannot modify this result.'))
    db.session.delete(result)
    db.session.commit()
    return jsonify({'status': 'ok'})
