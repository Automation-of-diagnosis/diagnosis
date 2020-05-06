import logging
from logging.config import dictConfig

from flask import Flask
from flask_login import LoginManager

from webapp.admin.views import blueprint as admin_blueprint
from webapp.gsc import funcs as funcs_gsc
from webapp.config import LOGGING
from webapp.gsc.forms import LoginForm
from webapp.api.views import blueprint as api_blueprint
from webapp.gsc.views import blueprint as gsc_blueprint
from webapp.model import my_app_db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    dictConfig(LOGGING)

    app = Flask(__name__)
    app.logger = logging.getLogger('my_app')
    app.logger.info('App started')
    # Доступ к переменным в config.py
    app.config.from_pyfile('config.py')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    # Доступ к переменным в config.py
    app.config.from_pyfile('config.py')
    # Подключение blueprint
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(gsc_blueprint)
    app.register_blueprint(user_blueprint)

    @app.route("/", methods=["GET", "POST"])
    def index():
        return funcs_gsc.index()

    # функция получающая по id объект пользователя
    @login_manager.user_loader
    def load_user(user_id):
        # Запрос к базе данных - получение по id объект пользователя
        return User.get(User.user_id == user_id)

    return app
