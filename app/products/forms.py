from flask_wtf import FlaskForm as Form
from wtforms import SubmitField, IntegerField, SelectField, StringField, BooleanField
from wtforms.fields.html5 import DateTimeField, DateField
from wtforms.validators import Required, NumberRange, InputRequired, Length
from flask_pagedown.fields import PageDownField
from flask_babel import gettext, lazy_gettext


class ProductForm(Form):
    id = IntegerField(lazy_gettext('Id'), render_kw={'readonly': True})
    date = StringField(lazy_gettext('Date Added'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, product):
        self.id.data = product.id
        self.date.data = product.date_added

    def to_model(self, product):
        product.id = self.id.data
        product.date_added = self.date.data


class CommentForm(Form):
    body = PageDownField(lazy_gettext('Comment'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))


class FindProductForm(Form):
    id = StringField(lazy_gettext('Id'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Find'))

    def __init__(self, type_choices):
        Form.__init__(self)
        #self.type.choices = type_choices


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
