from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from flask_babel import gettext
from flask_paginate import Pagination
from .. import db
from ..models import Operation
from . import operations

@operations.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['OPERATIONS_PER_PAGE']
    total = Operation.query.count()
    operations = Operation.query.order_by(Operation.id.desc()).paginate(page, per_page, False).items
    pagination = Pagination(page=page, total=total, record_name='operations', per_page=per_page)
    return render_template('operations/index.html', operations=operations, pagination=pagination)

@operations.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    operation = Operation.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(operation)
        db.session.commit()
        flash(gettext(u'Operation: {operation} has been deleted.'.format(operation=operation.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove operations.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('operations/index.html')
