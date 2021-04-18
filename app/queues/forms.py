from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, IPAddress, InputRequired
from flask_babel import gettext, lazy_gettext


class QueueForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    product_id = StringField(lazy_gettext('Product ID'), validators=[Optional(), Length(1, 64)])
    name = StringField(lazy_gettext('Name'), validators=[Optional(), Length(1, 16)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, queue):
        self.id.data = queue.id
        self.name.data = queue.name
        self.product_id.data = queue.product_id


    def to_model(self, queue):
        queue.id = self.id.data
        queue.name = self.name.data
        queue.product_id = self.product_id.data

    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))