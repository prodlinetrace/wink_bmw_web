from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from flask_babel import gettext
from flask_paginate import Pagination
from .. import db
from ..models import Status
from . import statuses

@statuses.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['STATUSES_PER_PAGE']
    total = Status.query.count()
    statuses = Status.query.order_by(Status.id.desc()).paginate(page, per_page, False).items
    pagination = Pagination(page=page, total=total, record_name='statuses', per_page=per_page, prev_label=gettext(u'Older'), next_label=gettext(u'Newer'))
    return render_template('statuses/index.html', statuses=statuses, pagination=pagination)

@statuses.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    status = Status.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(status)
        db.session.commit()
        flash(gettext(u'status: {status} has been deleted.'.format(status=status.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove statuses.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('statuses/index.html')
