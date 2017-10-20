from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from flask.ext.babel import gettext, lazy_gettext


class LoginForm(Form):
    username = StringField(lazy_gettext('Username'), validators=[Required(), Length(1, 64)])
    password = PasswordField(lazy_gettext('Password'), validators=[Required()])
    remember_me = BooleanField(lazy_gettext('Keep me logged on'))
    submit = SubmitField(lazy_gettext('Log In'))
