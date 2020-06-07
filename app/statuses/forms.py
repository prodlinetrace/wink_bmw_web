from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, IPAddress, InputRequired
from flask_babel import gettext, lazy_gettext


class StatusForm(Form):
    id = IntegerField(lazy_gettext('Id'), render_kw={'readonly': False})
    status = IntegerField(lazy_gettext('Status'), validators=[Required()])
    product_id = StringField(lazy_gettext('Product ID'), validators=[Required(), Length(1, 30)])
    station_id = IntegerField(lazy_gettext('Station ID'), validators=[Required()])
    user_id = IntegerField(lazy_gettext('User ID'), validators=[Optional()])
    program_number = IntegerField(lazy_gettext('Program Number'), validators=[Required()])
    nest_number = IntegerField(lazy_gettext('Nest Number'), validators=[Required()])
    date = StringField(lazy_gettext('Date Time'), validators=[Required(), Length(0, 40)])

    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, status):
        self.id.data = status.id
        self.status.data = status.status
        self.product_id.data = status.product_id
        self.station_id.data = status.station_id
        self.user_id.data = status.user_id
        self.program_number.data = status.program_number
        self.nest_number.data = status.nest_number
        self.date.data = status.date_time


    def to_model(self, status):
        status.id = self.id.data
        status.status = self.status.data 
        status.product_id = self.product_id.data
        status.station_id = self.station_id.data
        status.user_id = self.user_id.data
        status.program_number = self.program_number.data
        status.nest_number = self.nest_number.data
        status.date_time = self.date.data


    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))
                
                
    def __init__(self, new_item=False, id=None):
        Form.__init__(self)
        if new_item and id is not None:
            self.id.render_kw={'readonly': True}
            self.id.data = id
                