from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask_babel import gettext, lazy_gettext


class ResultForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 50)])
    description = StringField(lazy_gettext('Description'), validators=[Optional(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, result):
        self.id.data = result.id
        self.name.data = result.name
        self.description.data = result.description

    def to_model(self, result):
        result.id = self.id.data
        result.name = self.name.data
        result.description = self.description.data
