from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from flask_babel import gettext
from flask_paginate import Pagination
from .. import db
from ..models import Result
from . import results
from .forms import ResultForm


@results.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['OPERATION_TYPES_PER_PAGE']
    total = Result.query.count()
    results = Result.query.order_by(Result.id.desc()).paginate(page, per_page, False).items
    pagination = Pagination(page=page, total=total, record_name='results', per_page=per_page)
    return render_template('results/index.html', results=results, pagination=pagination)
    

@results.route('/<int:id>')
@login_required
def result(id):
    result = Result.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('results/result.html', result=result)


@results.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_result_id = Result.query.first()
    id = 1
    if _last_result_id is not None:
        id = _last_result_id.id + 1
    form = ResultForm()
    if form.validate_on_submit():
        result = Result(id)
        form.to_model(result)  # update result object with form data
        db.session.add(result)
        db.session.commit()
        flash(gettext(u'New result: {result} was added successfully.'.format(result=result.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    return render_template('results/new.html', form=form)


@results.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    result = Result.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = ResultForm()
    if form.validate_on_submit():
        form.to_model(result)
        db.session.add(result)
        db.session.commit()
        flash(gettext(u'Result with id: {result} has been updated.'.format(result=result.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(result)
    return render_template('results/edit.html', result=result, form=form)


@results.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    result = Result.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(result)
        db.session.commit()
        flash(gettext(u'Result with id: {result} has been deleted.'.format(result=result.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove results.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('results/index.html')
