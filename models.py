from typing import Dict

from peewee import (Model, SqliteDatabase, DoubleField, CharField, IntegerField, DateTimeField,
                    datetime as pw_datetime)

from config import DB_NAME

my_app_db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = my_app_db


class RequestUser(BaseModel):
    full_name = CharField()
    age = IntegerField()
    number = IntegerField()
    created = DateTimeField(default=pw_datetime.datetime.now())
    srAD = CharField()
    creatinine = IntegerField()
    bilirubin = IntegerField()
    platelets = IntegerField()
    pao2_fio2 = IntegerField()
    gsc = IntegerField()
    # eye_reaction = CharField()
    # motor_reaction = CharField()
    # speech = CharField()


class AppClass(BaseModel):
    data_from_user1 = IntegerField()
    data_from_user2 = DoubleField()
    data_from_user3 = CharField()
    created = DateTimeField(default=pw_datetime.datetime.now())

    def to_dict(self) -> Dict[str, str]:
        return self._data


# App_class.create_table(True)
RequestUser.create_table(True)
