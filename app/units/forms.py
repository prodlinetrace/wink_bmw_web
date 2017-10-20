from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask.ext.babel import gettext, lazy_gettext


class UnitForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 50)])
    symbol = StringField(lazy_gettext('Symbol'), validators=[Required(), Length(1, 16)])
    description = StringField(lazy_gettext('Description'), validators=[Optional(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, unit):
        self.id.data = unit.id
        self.name.data = unit.name
        self.symbol.data = unit.symbol
        self.description.data = unit.description

    def to_model(self, unit):
        unit.id = self.id.data
        unit.name = self.name.data
        unit.symbol = self.symbol.data
        unit.description = self.description.data
