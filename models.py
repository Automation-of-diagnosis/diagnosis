from peewee import (Model, SqliteDatabase, DoubleField, CharField, IntegerField, DateTimeField,
                    datetime as pw_datetime)

from config import DB_NAME

my_app_db = SqliteDatabase(DB_NAME)


class App_class(Model):
    class Meta:
        db = my_app_db

    data_from_user1 = IntegerField()
    data_from_user2 = DoubleField()
    data_from_user3 = CharField()
    created = DateTimeField(default=pw_datetime.datetime.now())

    def to_dict(self):
        return self._data


App_class.create_table(True)