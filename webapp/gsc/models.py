from peewee import (Model, SqliteDatabase, CharField, IntegerField, DateTimeField,
                    datetime as pw_datetime)

from webapp.config import DB_NAME

my_app_db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = my_app_db


class RequestUser(BaseModel):
    full_name = CharField(null=True)
    age = IntegerField(null=True)
    number = IntegerField(unique=True)
    created = DateTimeField(default=pw_datetime.datetime.now())
    srad = CharField(null=True)
    creatinine = IntegerField(null=True)
    bilirubin = IntegerField(null=True)
    platelets = IntegerField(null=True)
    pao2_fio2 = IntegerField(null=True)
    gsc = IntegerField(null=True)


RequestUser.create_table(True)
