from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask_babel import gettext, lazy_gettext


class DescriptionForm(Form):
    id = StringField(lazy_gettext('Id'), validators=[InputRequired(), Length(1, 20)])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 64)])
    display_format = StringField(lazy_gettext('Display Format'), validators=[Optional(), Length(1, 32)])
    description = StringField(lazy_gettext('Description'), validators=[Optional(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, description):
        self.id.data = description.id
        self.name.data = description.name
        self.display_format.data = description.display_format
        self.description.data = description.description

    def to_model(self, description):
        description.id = self.id.data
        description.name = self.name.data
        description.display_format = self.display_format.data
        description.description = self.description.data
