from flask import jsonify, g, flash
from flask.ext.babel import gettext
from .. import db
from ..models import Product, Status, Operation, Comment

from . import webapi
from .errors import forbidden, bad_request
from flask.ext.babel import gettext

@webapi.route('/products/<id>', methods=['DELETE'])
def delete_product(id):

    product = Product.query.filter_by(id=id).first()
    if product is None:
        abort(404)
    if not g.current_user.is_admin:
        return forbidden(gettext('You cannot modify this product.'))
    comments = Comment.query.filter_by(product_id=product.id)
    statuses = Status.query.filter_by(product_id=product.id)
    operations = Operation.query.filter_by(product_id=product.id)

    flash(gettext(u'Product: {product} removed with {comments_count} comments, {status_count} statuses and {operations_count} operations.'.format(product=product.id, operations_count=operations.count(), status_count=statuses.count(), comments_count=comments.count())))
    for to_remove in comments, statuses, operations:
        for item in to_remove:
            db.session.delete(item)
            # flash(gettext(u'Removing: {item}'.format(item=item)))

    db.session.delete(product)
    db.session.commit()
    return jsonify({'status': 'ok'})
