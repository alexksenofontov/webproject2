from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField, DateField, TimeField


class AddTimeForm(FlaskForm):
    doctor = StringField('Врач', validators=[DataRequired])
    date = DateField('Дата', validators=[DataRequired()])
    time1 = TimeField('Время начала работы', validators=[DataRequired()])
    time2 = TimeField('Время окончания работы', validators=[DataRequired()])
    submit2 = SubmitField('Добавить')