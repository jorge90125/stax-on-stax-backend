from flask import Flask, jsonify, after_this_request, g
from flask_login import LoginManager
import os
from dotenv import load_dotenv
load_dotenv()
from flask_cors import CORS
from resources.users import users
import models

DEBUG = True

PORT = os.environ.get('PORT')

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_APP_SECRET')
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

CORS(users, origins = ['http://localhost:3000'], supports_credentials = True)

app.register_blueprint(users, url_prefix = '/users')

@app.route('/')
def hello():
    return 'App works!'

if os.environ.get('FLASK_ENV') != 'development':
    print('\non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    print('Connected to the DB and created tables if they do not already exist.')
    app.run(debug = DEBUG, port = PORT)