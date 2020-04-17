from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField, DateField, TimeField


class AddRecForm(FlaskForm):
    record = StringField('Врач', validators=[DataRequired])
    submit = SubmitField('Записаться')