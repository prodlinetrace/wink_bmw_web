from flask import jsonify, g
from .. import db
from ..models import Comment

from . import webapi
from .errors import forbidden, bad_request
from flask.ext.babel import gettext

@webapi.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if comment.author_id != g.current_user.id and not g.current_user.is_admin:
        return forbidden(gettext('You cannot modify this comment.'))
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'status': 'ok'})
