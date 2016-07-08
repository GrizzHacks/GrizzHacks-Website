import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from flask_admin.contrib.peewee import ModelView
from peewee import *
from flask_peewee.admin import Admin
from flask_peewee.auth import Auth


DATABASE = SqliteDatabase('GrizzHacks.sqlite', check_same_thread=False)


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, email, password, admin=True):
        try:
            cls.create(
                email=email,
                password=generate_password_hash(password),
                is_admin=admin)
        except IntegrityError:
           raise ValueError("User already exists")


class Apply(Model):
        fullname = TextField(unique=False)
        emailapp = CharField (max_length=100)
        birthday = TextField()
        phone = TextField()
        graduation = TextField()
        gender = TextField()
        school = TextField()
        github = TextField()
        accept_tos = BooleanField()





def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Apply], safe=True)
    DATABASE.close()

