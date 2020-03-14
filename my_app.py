import logging
from logging.config import dictConfig

from flask import Flask

from config import LOGGING
# import views

dictConfig(LOGGING)

app = Flask(__name__)
app.logger = logging.getLogger("my_app")
app.logger.info("App started")