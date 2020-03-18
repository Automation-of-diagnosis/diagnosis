import logging
from logging.config import dictConfig

from flask import Flask

from config import LOGGING
from models import my_app_db

dictConfig(LOGGING)

app = Flask(__name__)
app.logger = logging.getLogger("my_app")
app.logger.info("App started")
# Доступ к переменным в config.py
app.config.from_pyfile('config.py')
# Инициализация базы данных
my_app_db.init_app(app)

import views
