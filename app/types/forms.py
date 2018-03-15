from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask_babel import gettext, lazy_gettext


class TypeForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 50)])
    symbol = StringField(lazy_gettext('Symbol'), validators=[Required(), Length(1, 16)])
    description = StringField(lazy_gettext('Description'), validators=[Optional(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, type):
        self.id.data = type.id
        self.name.data = type.name
        self.symbol.data = type.symbol
        self.description.data = type.description

    def to_model(self, type):
        type.id = self.id.data
        type.name = self.name.data
        type.symbol = self.symbol.data
        type.description = self.description.data
