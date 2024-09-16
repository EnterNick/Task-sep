from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, TelField, SelectField
from wtforms.validators import DataRequired


class SkillsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    submit = SubmitField('Применить')


class RegisterForm(FlaskForm):
    tel = TelField('Телефон', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    home = SelectField('Место проживания', validators=[DataRequired()], choices=[('P', 'Пирамида'), ('H', 'Хостел-2'),
                                                                                 ('S', 'Южный парк')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
