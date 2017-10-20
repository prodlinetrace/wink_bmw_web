from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, IPAddress, InputRequired
from flask.ext.babel import gettext, lazy_gettext


class StationForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    name = StringField(lazy_gettext('Name'), validators=[Optional(), Length(1, 64)])
    ip = StringField(lazy_gettext('IP Address'), validators=[Required(), IPAddress()])
    port = IntegerField(lazy_gettext('Port'), validators=[Optional()])
    rack = IntegerField(lazy_gettext('Rack'), validators=[Optional()])
    slot = IntegerField(lazy_gettext('Slot'), validators=[Optional()])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, station):
        self.id.data = station.id
        self.name.data = station.name
        self.ip.data = station.ip
        self.port.data = station.port
        self.rack.data = station.rack
        self.slot.data = station.slot

    def to_model(self, station):
        station.id = self.id.data
        station.name = self.name.data
        station.ip = self.ip.data
        station.port = self.port.data
        station.rack = self.rack.data
        station.slot = self.slot.data

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))