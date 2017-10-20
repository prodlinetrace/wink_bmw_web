from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from .. import db
from ..models import Program
from . import programs
from .forms import ProgramForm


@programs.route('/')
@login_required
def index():
    program_list = Program.query.order_by(Program.id.desc())
    return render_template('programs/index.html', programs=program_list)


@programs.route('/<id>')
@login_required
def program(id):
    program = Program.query.filter_by(id=id).first_or_404()
    return render_template('programs/program.html', program=program)


@programs.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_program_id = Program.query.first()
    id = 1
    if _last_program_id is not None:
        id = _last_program_id.id + str(1)
    form = ProgramForm()
    if form.validate_on_submit():
        program = Program(id)
        form.to_model(program)  # update program object with form data
        db.session.add(program)
        db.session.commit()
        flash(gettext(u'New program: {program} was added successfully.'.format(program=program.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
    return render_template('programs/new.html', form=form)


@programs.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    program = Program.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = ProgramForm()
    if form.validate_on_submit():
        form.to_model(program)
        db.session.add(program)
        db.session.commit()
        flash(gettext(u'Program with id: {program} has been updated.'.format(program=program.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(program)
    return render_template('programs/edit.html', program=program, form=form)


@programs.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    program = Program.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(program)
        db.session.commit()
        flash(gettext(u'Program with id: {id} has been deleted.'.format(id=program.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove programs.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('programs/index.html')
