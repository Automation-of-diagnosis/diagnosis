import logging
from logging.config import dictConfig

from flask import Flask

from webapp.gsc import funcs as funcs_gsc
from webapp.config import LOGGING
from webapp.gsc.forms import LoginForm
from webapp.api.views import blueprint as api_blueprint
from webapp.gsc.views import blueprint as gsc_blueprint
from webapp.model import my_app_db


def create_app():
    dictConfig(LOGGING)

    app = Flask(__name__)
    app.logger = logging.getLogger('my_app')
    app.logger.info('App started')
    # Доступ к переменным в config.py
    app.config.from_pyfile('config.py')

    app.logger.info('App started')
    # Доступ к переменным в config.py
    app.config.from_pyfile('config.py')
    # Подключение blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(gsc_blueprint)

    @app.route("/", methods=["GET", "POST"])
    def index():
        return funcs_gsc.index()

    return app
