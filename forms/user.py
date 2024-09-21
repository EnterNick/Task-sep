from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, TelField,
                     SelectField)
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
    home = SelectField('Место проживания', validators=[DataRequired()], choices=[('Пирамида', 'Пирамида'),
                                                                                 ('Хостел', 'Хостел'),
                                                                                 ('Южный Парк', 'Южный Парк')])
    submit = SubmitField('Зарегистрироваться')


class EditForm(FlaskForm):
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    name = StringField('Имя пользователя', validators=[DataRequired()])
    home = SelectField('Место проживания', validators=[DataRequired()], choices=[('Пирамида', 'Пирамида'),
                                                                                 ('Хостел', 'Хостел'),
                                                                                 ('Южный Парк', 'Южный Парк')])
    submit = SubmitField('Сохранить')


class LoginForm(FlaskForm):
    tel = TelField('Телефон', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SubForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Подписаться')


class SearchForm(FlaskForm):
    search = StringField('Искать здесь...')
    submit = SubmitField('🔍')


class FeedbackForm(FlaskForm):
    input = StringField('Оставить отзыв')
    submit = SubmitField('➤')