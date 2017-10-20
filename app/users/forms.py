from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField, SelectField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import Optional, Length, Required, EqualTo
from flask.ext.pagedown.fields import PageDownField
from flask.ext.babel import gettext, lazy_gettext
from .. import cfg
languages = cfg['default'].LANGUAGES


class ProfileForm(Form):
    name = StringField(lazy_gettext('Name'), validators=[Optional(), Length(1, 64)])
    location = StringField(lazy_gettext('Location'), validators=[Optional(), Length(1, 64)])
    locale = SelectField(lazy_gettext('Locale'), validators=[Optional()], choices=languages)
    bio = TextAreaField(lazy_gettext('Bio'))
    password = PasswordField(lazy_gettext('Password'), validators=[Required(), EqualTo(gettext('confirm'), message=gettext('Passwords must match'))])
    confirm = PasswordField(lazy_gettext('Repeat Password'))
    submit = SubmitField(lazy_gettext('Submit'))


class UserForm(Form):
    login = StringField(lazy_gettext('Login'), validators=[Required(), Length(1, 64)])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 64)])
    password = PasswordField(lazy_gettext('Password'), validators=[Required(), EqualTo(gettext('confirm'), message=gettext('Passwords must match'))])
    confirm = PasswordField(lazy_gettext('Repeat Password'))
    operator = BooleanField(lazy_gettext('Operator'), default=True)
    admin = BooleanField(lazy_gettext('Administrator'), default=False)
    submit = SubmitField(lazy_gettext('Submit'))

class PasswordForm(Form):
    login = HiddenField(lazy_gettext('Login'))
    password = PasswordField(lazy_gettext('Password'), validators=[Required(), EqualTo(gettext('confirm'), message=gettext('Passwords must match'))])
    confirm = PasswordField(lazy_gettext('Repeat Password'))
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, user):
        self.login.data = user.login

    def to_model(self, user):
        user.login = self.login.data
        user.password = self.password.data

class EditUserForm(Form):
    id = StringField(lazy_gettext('Id'), validators=[Required()])
    login = StringField(lazy_gettext('Login'), validators=[Required(), Length(1, 64)])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 64)])
    location = StringField(lazy_gettext('Location'), validators=[Optional(), Length(1, 64)])
    locale = SelectField(lazy_gettext('Locale'), validators=[Optional()], choices=languages)
    bio = TextAreaField(lazy_gettext('Bio'), validators=[Optional()])
    operator = BooleanField(lazy_gettext('Operator'), default=True)
    admin = BooleanField(lazy_gettext('Administrator'), default=False)
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, user):
        self.id.data = int(user.id)
        self.login.data = user.login
        self.name.data = user.name
        self.location.data = user.location
        self.locale.data = user.locale
        self.bio.data = user.bio
        if self.admin:
            self.admin.data = user.is_admin
        if self.operator:
            self.operator.data = user.is_operator


    def to_model(self, user):
        user.id = int(self.id.data)
        user.login = self.login.data
        user.name = self.name.data
        user.location = self.location.data
        user.locale = self.locale.data
        user.bio = self.bio.data
        if self.admin:
            user.is_admin = self.admin.data
        if self.operator:
            user.is_operator = self.operator.data
            
