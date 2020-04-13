import logging
from logging.config import dictConfig

from flask import Flask

from webapp.gsc import funcs as funcs_gsc
from webapp.config import LOGGING
from webapp.gsc.forms import LoginForm
from webapp.gsc.views import blueprint as gsc_blueprint


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
    # Подключение blueprint
    app.register_blueprint(gsc_blueprint)

    @app.route("/", methods=["GET", "POST"])
    def index():
        return funcs_gsc.index()

    return app
