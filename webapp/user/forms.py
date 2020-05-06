from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    # default=True - галочка в чекбоксе по умолчанию отмечена. Поле для "запоминания" пользователя после закрытия сайта
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form_check_input"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    # test@example.com - безопасная почта для тестирования
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        for data in User.select():
            if data.username == username:
                raise ValidationError('Пользователь с таким именем уже зарегистрирован')

    def validate_email(self, email):
        for data in User.select():
            if data.email == email:
                raise ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')
