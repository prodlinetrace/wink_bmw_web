from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from .. import db
from ..models import User, Comment
from . import users
from .forms import ProfileForm, UserForm, EditUserForm, PasswordForm
from flask_babel import gettext
from flask_paginate import Pagination
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort


def get_object_or_404(model, *criterion):
    try:
        return model.query.filter(*criterion).one()
    except exc.NoResultFound:
        abort(404)
    except exc.MultipleResultsFound:
        abort(404)


@users.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['USERS_PER_PAGE']
    total = User.query.count()
    users = User.query.order_by(User.login.desc()).paginate(page, per_page, False).items
    pagination = Pagination(page=page, total=total, record_name='users', per_page=per_page)
    return render_template('users/index.html', users=users, pagination=pagination)

    
@users.route('/<login>')
@login_required
def user(login):
    user = User.query.filter_by(login=login).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['COMMENTS_PER_PAGE']
    total = user.comments.count()
    comments = user.comments.paginate(page, per_page, False).items
    pagination = Pagination(page=page, total=total, record_name='comments', per_page=per_page)
    return render_template('users/user.html', user=user, comments=comments, pagination=pagination)

    
@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.locale = form.locale.data
        current_user.bio = form.bio.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash(gettext(u'{user}, you have updated your profile successfully.'.format(user=current_user.name)))
        return redirect(url_for('users.user', login=current_user.login))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.locale.data = current_user.locale
    form.bio.data = current_user.bio
    return render_template('users/profile.html', form=form)

@users.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    form = UserForm()
    if form.validate_on_submit():
        user = User(login=form.login.data, name=form.name.data, password=form.password.data, is_admin=form.admin.data, is_operator=form.operator.data)
        db.session.add(user)
        db.session.commit()
        flash(gettext(u'New user: {user} was added successfully.'.format(user=user.name)))
        return redirect(url_for('.index'))
    return render_template('users/new_user.html', form=form)


@users.route('/edit/<login>', methods=['GET', 'POST'])
@login_required
def edit(login):
    user = get_object_or_404(User, User.login == login)
    if not current_user.is_admin and user.login != current_user.login:
        abort(403)
    form = EditUserForm()
    if not current_user.is_admin:
        del form.admin
    if form.validate_on_submit():
        form.to_model(user)
        db.session.add(user)
        db.session.commit()
        flash(gettext(u'User profile for: {user} has been updated.'.format(user=user.name)))
        return redirect(url_for('.index'))
    form.from_model(user)
    return render_template('users/profile.html', form=form)


@users.route('/password/<login>', methods=['GET', 'POST'])
@login_required
def password(login):
    user = get_object_or_404(User, User.login == login)
    if not current_user.is_admin and user.login != current_user.login:
        abort(403)
    form = PasswordForm()
    if form.validate_on_submit():
        form.to_model(user)
        db.session.add(user)
        db.session.commit()
        flash(gettext(u'User password for: {user} has been updated.'.format(user=user.name)))
        return redirect(url_for('.index'))
    form.from_model(user)
    return render_template('users/password.html', form=form)


@users.route('/delete/<login>', methods=['GET', 'POST'])
@login_required
def delete(login):
    user = get_object_or_404(User, User.login == login)
    if current_user.is_admin:
        if user.login == current_user.login:
            flash(gettext(u'Unable to remove currently logged user: {user}.'.format(user=user.name)))
            return redirect(url_for('.index'))

        db.session.delete(user)
        db.session.commit()
        flash(gettext(u'User profile for: {user} has been deleted.'.format(user=user.name)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be adminstrator to remove users.'.format(user=user.name)))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('users/index.html')
