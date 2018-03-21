from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask_babel import gettext, lazy_gettext
import six


class ResultForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    product_id = SelectField(lazy_gettext('Product'))
    station_id = SelectField(lazy_gettext('Station'), coerce=int)
    operation_id = SelectField(lazy_gettext('Operation'), coerce=int)
    unit_id = SelectField(lazy_gettext('Unit'), coerce=int)
    type_id = SelectField(lazy_gettext('Type'), coerce=int)
    desc_id = SelectField(lazy_gettext('Desc'), coerce=int)
    value = StringField(lazy_gettext('Value'), validators=[Required(), Length(1, 50)])

    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, result):
        self.id.data = result.id
        self.product_id.data = six.u(result.product_id)
        self.station_id.data = six.u(result.station_id)
        self.operation_id.data = six.u(result.operation_id)
        self.unit_id.data = six.u(result.unit_id)
        self.type_id.data = six.u(result.type_id)
        self.desc_id.data = six.u(result.desc_id)
        self.value.data = result.value

 
    def to_model(self, result):
        result.id = self.id.data
        result.product_id = six.u(self.product_id.data)
        result.station_id = six.u(self.station_id.data)
        result.operation_id = six.u(self.operation_id.data)
        result.unit_id = six.u(self.unit_id.data)
        result.type_id = six.u(self.type_id.data)
        result.desc_id = six.u(self.desc_id.data)
        result.value = self.value.data

    def __init__(self, product_choices, station_choices, operation_choices, unit_choices, type_choices, desc_choices):
        Form.__init__(self)
        self.product_id.choices = product_choices
        self.station_id.choices = station_choices
        self.operation_id.choices = operation_choices
        self.unit_id.choices = unit_choices
        self.type_id.choices = type_choices
        self.desc_id.choices = desc_choices
