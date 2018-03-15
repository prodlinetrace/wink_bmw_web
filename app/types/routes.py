from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from flask_babel import gettext
from .. import db
from ..models import Type
from . import types
from .forms import TypeForm


@types.route('/')
@login_required
def index():
    type_list = Type.query.order_by(Type.id.desc())
    return render_template('types/index.html', types=type_list)


@types.route('/<int:id>')
@login_required
def type(id):
    type = Type.query.filter_by(id=id).first_or_404()
    return render_template('types/type.html', type=type)


@types.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_type_id = Type.query.first()
    id = 1
    if _last_type_id is not None:
        id = _last_type_id.id + 1
    form = TypeForm()
    if form.validate_on_submit():
        type = Type(id)
        form.to_model(type)  # update type object with form data
        db.session.add(type)
        db.session.commit()
        flash(gettext(u'New type: {type} was added successfully.'.format(type=type.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
    return render_template('types/new.html', form=form)


@types.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    type = Type.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = TypeForm()
    if form.validate_on_submit():
        form.to_model(type)
        db.session.add(type)
        db.session.commit()
        flash(gettext(u'Type with id: {type} has been updated.'.format(type=type.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(type)
    return render_template('types/edit.html', type=type, form=form)


@types.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    type = Type.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(type)
        db.session.commit()
        flash(gettext(u'Type with id: {id} has been deleted.'.format(id=type.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove types.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('types/index.html')
