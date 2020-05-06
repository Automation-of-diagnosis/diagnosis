# UserMixin содержит проверку авторизации
from peewee import CharField
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.model import BaseModel


class User(BaseModel, UserMixin):
    username = CharField(null=True, unique=True)
    password = CharField(null=True)
    role = CharField(null=True)
    email = CharField(null=True, unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # @property позволяет вызывать метод как атрибут (без скобочек)
    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}, id {}>'.format(self.username, self.id)
