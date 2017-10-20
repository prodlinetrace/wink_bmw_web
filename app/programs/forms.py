from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask.ext.babel import gettext, lazy_gettext


class ProgramForm(Form):
    id = StringField(lazy_gettext('Id'), validators=[InputRequired(), Length(1, 20)])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 50)])
    description = StringField(lazy_gettext('Description'), validators=[Optional(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, program):
        self.id.data = program.id
        self.name.data = program.name
        self.description.data = program.description

    def to_model(self, program):
        program.id = self.id.data
        program.name = self.name.data
        program.description = self.description.data
