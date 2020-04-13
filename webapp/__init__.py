import logging
from logging.config import dictConfig

from flask import Flask, request

from webapp.gsc import funcs as funcs_gsc
from webapp.config import LOGGING
from webapp.gsc.forms import LoginForm


def create_app():
    dictConfig(LOGGING)

    app = Flask(__name__)
    app.logger = logging.getLogger('my_app')
    app.logger.info('App started')
    # Доступ к переменным в config.py
    app.config.from_pyfile('config.py')
    # Инициализация базы данных
    app.logger.info('App started')
    # Доступ к переменным в config.py
    app.config.from_pyfile('config.py')

    @app.route("/", methods=["GET", "POST"])
    def index():
        return funcs_gsc.index()

    @app.route("/choice", methods=["GET", "POST"])
    def choice():
        choice_user = request.form['index']
        if choice_user == 'New':
            return funcs_gsc.index()
        else:
            return funcs_gsc.add_data(int(choice_user))

    @app.route("/add_data", methods=["GET", "POST"])
    def add_data():
        return funcs_gsc.update_db()

    return app
