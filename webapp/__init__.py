import logging
from logging.config import dictConfig
from flask_migrate import Migrate

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
    # Инициализация базы данных
    app.logger.info('App started')
    # Доступ к переменным в config.py
    app.config.from_pyfile('config.py')
    # Подключение blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(gsc_blueprint)
    # Создаём объект класса Migrate передавая ему app and my_app_db
    migrate = Migrate(app, my_app_db)
    # export FLASK_APP=webapp && flask db init --> команда "инициализации" миграций
    # mv my_app.db my_app.db.old - переименование (копирование) базы данных
    # export FLASK_APP=webapp && flask db migrate -m "что сделано" --> создание миграции
    # flask db upgrade --> подтвердить миграцию
    # mv my_app.db.old my_app.db --> переписать старые данные в новую базу и удалить базу из которой переносим
    # flask my_app_db stamp {Revision number from migration version} - применить миграцию к уже существующей

    @app.route("/", methods=["GET", "POST"])
    def index():
        return funcs_gsc.index()

    return app
