from peewee import (CharField, IntegerField, DateTimeField, datetime as pw_datetime)

from webapp.model import BaseModel


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
