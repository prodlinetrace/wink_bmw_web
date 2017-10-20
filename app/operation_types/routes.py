from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from flask.ext.paginate import Pagination
from .. import db
from ..models import Operation_Type
from . import operation_types
from .forms import Operation_TypeForm


@operation_types.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['OPERATION_TYPES_PER_PAGE']
    total = Operation_Type.query.count()
    operation_types = Operation_Type.query.order_by(Operation_Type.id.desc()).paginate(page, per_page, False).items
    pagination = Pagination(page=page, total=total, record_name='operation_types', per_page=per_page)
    return render_template('operation_types/index.html', operation_types=operation_types, pagination=pagination)
    

@operation_types.route('/<int:id>')
@login_required
def operation_type(id):
    operation_type = Operation_Type.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('operation_types/operation_type.html', operation_type=operation_type)


@operation_types.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_operation_type_id = Operation_Type.query.first()
    id = 1
    if _last_operation_type_id is not None:
        id = _last_operation_type_id.id + 1
    form = Operation_TypeForm()
    if form.validate_on_submit():
        operation_type = Operation_Type(id)
        form.to_model(operation_type)  # update operation_type object with form data
        db.session.add(operation_type)
        db.session.commit()
        flash(gettext(u'New operation_type: {operation_type} was added successfully.'.format(operation_type=operation_type.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    return render_template('operation_types/new.html', form=form)


@operation_types.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    operation_type = Operation_Type.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = Operation_TypeForm()
    if form.validate_on_submit():
        form.to_model(operation_type)
        db.session.add(operation_type)
        db.session.commit()
        flash(gettext(u'Operation_Type with id: {operation_type} has been updated.'.format(operation_type=operation_type.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(operation_type)
    return render_template('operation_types/edit.html', operation_type=operation_type, form=form)


@operation_types.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    operation_type = Operation_Type.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(operation_type)
        db.session.commit()
        flash(gettext(u'Operation_Type with id: {operation_type} has been deleted.'.format(operation_type=operation_type.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove operation_types.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('operation_types/index.html')
