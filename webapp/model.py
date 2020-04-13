from peewee import (Model, SqliteDatabase)

from webapp.config import DB_NAME

my_app_db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = my_app_db
