from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from .. import db
from ..models import Unit
from . import units
from .forms import UnitForm


@units.route('/')
@login_required
def index():
    unit_list = Unit.query.order_by(Unit.id.desc())
    return render_template('units/index.html', units=unit_list)


@units.route('/<int:id>')
@login_required
def unit(id):
    unit = Unit.query.filter_by(id=id).first_or_404()
    return render_template('units/unit.html', unit=unit)


@units.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_unit_id = Unit.query.first()
    id = 1
    if _last_unit_id is not None:
        id = _last_unit_id.id + 1
    form = UnitForm()
    if form.validate_on_submit():
        unit = Unit(id)
        form.to_model(unit)  # update unit object with form data
        db.session.add(unit)
        db.session.commit()
        flash(gettext(u'New unit: {unit} was added successfully.'.format(unit=unit.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
    return render_template('units/new.html', form=form)


@units.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    unit = Unit.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = UnitForm()
    if form.validate_on_submit():
        form.to_model(unit)
        db.session.add(unit)
        db.session.commit()
        flash(gettext(u'Unit with id: {unit} has been updated.'.format(unit=unit.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(unit)
    return render_template('units/edit.html', unit=unit, form=form)


@units.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    unit = Unit.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(unit)
        db.session.commit()
        flash(gettext(u'Unit with id: {id} has been deleted.'.format(id=unit.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove units.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('units/index.html')
