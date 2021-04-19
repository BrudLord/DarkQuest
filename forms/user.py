from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Как звать тебя, странник?', validators=[DataRequired()])
    password = PasswordField('Секретный пароль', validators=[DataRequired()])
    password_again = PasswordField('Повтори его', validators=[DataRequired()])
    reg = SubmitField('Вступить в гильдию кашеваров')


class LoginForm(FlaskForm):
    name = StringField('Как звать тебя, странник?', validators=[DataRequired()])
    password = PasswordField('Секретный пароль', validators=[DataRequired()])
    log = SubmitField('Войти')
