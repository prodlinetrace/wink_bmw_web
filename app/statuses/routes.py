from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from flask_babel import gettext
from flask_paginate import Pagination
from .. import db
from ..models import Status
from . import statuses
from .forms import StatusForm


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

@statuses.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    status = Status.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = StatusForm()
    if form.validate_on_submit():
        form.to_model(status)
        db.session.add(status)
        db.session.commit()
        flash(gettext(u'Status profile for: {status} has been updated.'.format(status=status.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(status)
    return render_template('statuses/edit.html', status=status, form=form)

@statuses.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_status_id = Status.query.order_by(Status.id.desc()).first()
    i = 1
    if _last_status_id is not None:
        i = _last_status_id.id + 1

    form = StatusForm(True, i)
    if form.validate_on_submit():
        # TODO check if this does not break PK constraints.
        status = Status(i, 1, 1, 1, 1)
        form.to_model(status)  # update status object with form data
        db.session.add(status)
        db.session.commit()
        flash(gettext(u'New status: {status} was added successfully.'.format(status=status.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))

    return render_template('statuses/new.html', form=form)
