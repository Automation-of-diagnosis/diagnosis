# getpass скрывает ввод пароля с экрана
from getpass import getpass
import sys

from webapp import create_app
from webapp.user.models import User

app = create_app()

# app.app_context() - позволяет работать с базой данных
with app.app_context():
    username = input('Введите имя пользователя: ')

    if User.get_or_none(User.username == username):
        print('Такой пользователь уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password)
    new_user.save()
    print('Пользователь с id={} добавлен в таблицу базы данных'.format(new_user.id))
