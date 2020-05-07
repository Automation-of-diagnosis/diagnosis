# flash - позволяет передавать сообщения между route-ами (со страницы на страницу)
# redirect - даёт перенаправление пользователя на другую страницу
# url_for - помогает получить url по имени функции, которая этот url обрабатывает
from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        # если пользователь авторизован - перенаправлять его на страницу с которой он пришёл
        return redirect(get_redirect_target())
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.get(User.username == form.username.data)
        if user and user.check_password(form.password.data):
            # remember=form.remember_me.data - возвращает True or False в зависимости от галочки в чек-боксе
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))
            # return redirect(url_for(get_redirect_target()))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect((url_for('index')))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Регистрация'
    form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        # set_password - создать пароль
        new_user.set_password(form.password.data)
        new_user.save()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for fields, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}" - {}'.format(getattr(form, fields).label.text, error))
        return redirect(url_for('user.register'))
