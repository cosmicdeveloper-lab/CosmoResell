from quart_wtf import QuartForm
from wtforms import StringField, FloatField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class MyForm(QuartForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    source = SelectField('Source', choices=[('facebook', 'Facebook'), ('ebay', 'Ebay')], validators=[DataRequired()])
    threshold = FloatField('Threshold', validators=[DataRequired(message='threshold must be float'), NumberRange(max=0.9)])
    max_pages = IntegerField('Max Pages', validators=[DataRequired(), NumberRange(min=1)])
