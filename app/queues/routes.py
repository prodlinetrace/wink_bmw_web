from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from flask_babel import gettext
from flask_paginate import Pagination
from .. import db
from ..models import Queue
from . import queues
from .forms import QueueForm


@queues.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['STATIONS_PER_PAGE']
    total = Queue.query.count()
    queues = Queue.query.order_by(Queue.id.desc()).paginate(page, per_page, False).items
    pagination = Pagination(page=page, total=total, record_name='queues', per_page=per_page)
    return render_template('queues/index.html', queues=queues, pagination=pagination)

    page = request.args.get('page', 1, type=int)
    pagination = Queue.query.order_by(Queue.id.desc()).paginate(
        page, per_page=current_app.config['STATIONS_PER_PAGE'],
        error_out=False)
    queue_list = pagination.items
    return render_template('queues/index.html', queues=queue_list, pagination=pagination)


@queues.route('/<int:id>')
@login_required
def queue(id):
    queue = Queue.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('queues/queue.html', queue=queue)


@queues.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_station_id = Queue.query.first()
    id = 1
    if _last_station_id is not None:
        id = _last_station_id.id + 1

    form = QueueForm()
    if form.validate_on_submit():
        queue = Queue(id)
        form.to_model(queue)  # update queue object with form data
        db.session.add(queue)
        db.session.commit()
        flash(gettext(u'New queue: {queue} was added successfully.'.format(queue=queue.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))

    return render_template('queues/new.html', form=form)


@queues.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    queue = Queue.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = QueueForm()
    if form.validate_on_submit():
        form.to_model(queue)
        db.session.add(queue)
        db.session.commit()
        flash(gettext(u'Queue profile for: {queue} has been updated.'.format(queue=queue.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(queue)
    return render_template('queues/edit.html', queue=queue, form=form)


@queues.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    queue = Queue.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(queue)
        db.session.commit()
        flash(gettext(u'Queue for: {queue} has been deleted.'.format(queue=queue.name)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be adminstrator to remove queues.'.format(queue=queue.name)))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('queues/index.html')
