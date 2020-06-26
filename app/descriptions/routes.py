from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from flask_babel import gettext
from .. import db
from ..models import Desc
from . import descriptions
from .forms import DescriptionForm


@descriptions.route('/')
@login_required
def index():
    description_list = Desc.query.order_by(Desc.id.desc())
    return render_template('descriptions/index.html', descriptions=description_list)


@descriptions.route('/<id>')
@login_required
def description(id):
    description = Desc.query.filter_by(id=id).first_or_404()
    return render_template('descriptions/description.html', description=description)


@descriptions.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_description_id = Desc.query.first()
    id = 1
    if _last_description_id is not None:
        id = _last_description_id.id + 1
    form = DescriptionForm()
    if form.validate_on_submit():
        description = Desc(id)
        form.to_model(description)  # update description object with form data
        db.session.add(description)
        db.session.commit()
        flash(gettext(u'New description: {description} was added successfully.'.format(description=description.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
    return render_template('descriptions/new.html', form=form)


@descriptions.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    description = Desc.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = DescriptionForm()
    if form.validate_on_submit():
        form.to_model(description)
        db.session.add(description)
        db.session.commit()
        flash(gettext(u'Description with id: {description} has been updated.'.format(description=description.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(description)
    return render_template('descriptions/edit.html', description=description, form=form)


@descriptions.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    description = Desc.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(description)
        db.session.commit()
        flash(gettext(u'Description with id: {id} has been deleted.'.format(id=description.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove descriptions.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('descriptions/index.html')
