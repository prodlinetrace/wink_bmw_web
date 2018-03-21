from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask_babel import gettext, lazy_gettext
import six


class OperationForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    product_id = SelectField(lazy_gettext('Product'))
    station_id = SelectField(lazy_gettext('Station'), coerce=int)
    operation_status_id = SelectField(lazy_gettext('Operation'), coerce=int)
    operation_type_id = SelectField(lazy_gettext('Unit'), coerce=int)
    program_number = StringField(lazy_gettext('Program Number'), validators=[Required(), Length(1, 50)])
    nest_number = StringField(lazy_gettext('Nest Number'), validators=[Required(), Length(1, 50)])
    date_time = StringField(lazy_gettext('Date'), validators=[Required(), Length(1, 50)])

    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, operation):
        self.id.data = operation.id
        self.product_id.data = six.u(operation.product_id)
        self.station_id.data = six.u(operation.station_id)
        self.operation_status_id.data = six.u(operation.operation_status_id)
        self.operation_type_id.data = six.u(operation.operation_type_id)
        self.program_number.data = six.u(operation.program_number)
        self.nest_number.data = six.u(operation.nest_number)
        self.date_time.data = operation.date_time

 
    def to_model(self, operation):
        operation.id = self.id.data
        operation.product_id = six.u(self.product_id.data)
        operation.station_id = six.u(self.station_id.data)
        operation.operation_status_id = six.u(self.operation_status_id.data)
        operation.operation_type_id = six.u(self.operation_type_id.data)
        operation.program_number = six.u(self.program_number.data)
        operation.nest_number = six.u(self.nest_number.data)
        operation.date_time = self.date_time.data

    def __init__(self, product_choices, station_choices, operation_status_choices, operation_type_choices):
        Form.__init__(self)
        self.product_id.choices = product_choices
        self.station_id.choices = station_choices
        self.operation_status_id.choices = operation_status_choices
        self.operation_type_id.choices = operation_type_choices
