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

@operations.route('/<int:id>')
@login_required
def operation(id):
    operation = Operation.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('operations/operation.html', operation=operation)


@operations.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_operation_id = Operation.query.first()
    id = 1
    if _last_operation_id is not None:
        id = _last_operation_id.id + 1
    form = OperationForm()
    if form.validate_on_submit():
        operation = Operation(id)
        form.to_model(operation)  # update operation object with form data
        db.session.add(operation)
        db.session.commit()
        flash(gettext(u'New operation: {operation} was added successfully.'.format(operation=operation.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    return render_template('operations/new.html', form=form)


@operations.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    operation = Operation.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = OperationForm()
    if form.validate_on_submit():
        form.to_model(operation)
        db.session.add(operation)
        db.session.commit()
        flash(gettext(u'Operation with id: {operation} has been updated.'.format(operation=operation.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(operation)
    return render_template('operations/edit.html', operation=operation, form=form)
