from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask.ext.babel import gettext, lazy_gettext
from ..models import Unit
import six


class Operation_StatusForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 50)])
    unit_id = SelectField(lazy_gettext('Unit'))
    description = StringField(lazy_gettext('Description'), validators=[Optional(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, status):
        self.id.data = status.id
        self.name.data = status.name
        self.unit_id.data = six.u(status.unit_id)
        self.description.data = status.description

    def to_model(self, status):
        status.id = self.id.data
        status.name = self.name.data
        status.unit_id = six.u(self.unit_id.data)
        status.description = self.description.data
    
    def __init__(self, unit_choices):
        Form.__init__(self)
        self.unit_id.choices = unit_choices
        
