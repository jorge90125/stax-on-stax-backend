from peewee import *
import datetime
from flask_login import UserMixin
import os
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
  DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('stax_on_stax.sqlite')

class User(UserMixin, Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()

    class Meta:
        database = DATABASE

class Record(Model):
    name = CharField()
    artist = CharField()
    artwork_url = CharField()
    release_year = IntegerField()
    pressing_year = IntegerField()
    genre = CharField()
    record_label = CharField()
    catalog_num = CharField()
    country = CharField()
    favorite = BooleanField(default = False)
    owner = ForeignKeyField(User, backref='records')
    created_at = DateTimeField(default = datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()

    DATABASE.create_tables([User, Record], safe = True)
    DATABASE.close()