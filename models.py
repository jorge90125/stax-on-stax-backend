from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('stax_on_stax.sqlite')

class User(UserMixin, Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()

    DATABASE.create_tables([User], safe = True)
    DATABASE.close()