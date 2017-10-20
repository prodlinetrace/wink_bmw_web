from flask import render_template, current_app, request, redirect, url_for, flash
from flask_babel import gettext
from flask_login import login_user, logout_user, login_required
from ..models import User
from . import auth
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_app.config['DEBUG'] and not current_app.config['TESTING'] and not request.is_secure:
        return redirect(url_for('.login', _external=True, _scheme='https'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash(gettext('Invalid username or password.'))
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('products.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(gettext('You have been logged out.'))
    return redirect(url_for('products.index'))
