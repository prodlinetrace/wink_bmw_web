from flask.ext.wtf import Form
from wtforms import SubmitField, IntegerField, SelectField, StringField, BooleanField
from wtforms.fields.html5 import DateTimeField, DateField
from wtforms.validators import Required, NumberRange, InputRequired, Length
from flask.ext.pagedown.fields import PageDownField
from flask.ext.babel import gettext, lazy_gettext
#from wtforms.fields.simple import 


class ProductForm(Form):
    type = StringField(lazy_gettext('Product Type'), validators=[Required(), Length(1, 10)])
    serial = StringField(lazy_gettext('Serial Number'), validators=[Required(), Length(1, 20)])
    date = StringField(lazy_gettext('Date Added'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, product):
        self.type.data = product.type
        self.serial.data = product.serial
        self.date.data = product.date_added

    def to_model(self, product):
        product.type = self.type.data
        product.serial = self.serial.data
        product.date_added = self.date.data


class CommentForm(Form):
    body = PageDownField(lazy_gettext('Comment'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))


class FindProductForm(Form):
    type = SelectField(lazy_gettext('Product Type'), validators=[Required()])
    serial = StringField(lazy_gettext('Serial Number'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Find'))

    def __init__(self, type_choices):
        Form.__init__(self)
        self.type.choices = type_choices


class FindProductsRangeForm(Form):
    start = StringField(lazy_gettext('From'))
    end = StringField(lazy_gettext('To'))
    status_failed = BooleanField(lazy_gettext('Status Failed'))
    operation_failed = BooleanField(lazy_gettext('Operation Failed'))
    submit = SubmitField(lazy_gettext('Find'))


class HandScannerSearchForm(Form):
    product = StringField(lazy_gettext('Scan Product'))
    new_window = BooleanField(lazy_gettext('New Window'))
    submit = SubmitField(lazy_gettext('Find'))
    
    def __init__(self):
        Form.__init__(self)
        self.submit.id='product_button'


class ExportProductsRangeForm(Form):
    start = StringField(lazy_gettext('From'))
    end = StringField(lazy_gettext('To'))
    type = SelectField(lazy_gettext('Operation Type'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Find'))
        
    def __init__(self, type_choices):
        Form.__init__(self)
        self.type.choices = type_choices
