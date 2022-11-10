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

app.secret_key = os.environ.get('APP_SECRET')
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

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)


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