from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField, DateField


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    fam = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    fname = StringField('Отчество', validators=[DataRequired()])
    birth = DateField('Дата рождения', validators=[DataRequired()])
    polis = StringField('Серия и номер полиса (без пробелов)', validators=[DataRequired()])
    submit = SubmitField('Регистрация')