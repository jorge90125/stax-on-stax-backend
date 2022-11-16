import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

# REGISTER ROUTE
@users.route('/register', methods = ['POST'])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data = {}, status = {'code': 401, 'message': 'A user with that email already exists!'}),401
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict)
        
        del user_dict['password']

        return jsonify(data = user_dict, status = {'code': 201, 'message': 'Success'}), 201

# LOGIN ROUTE
@users.route('/login', methods = ['POST'])
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            return jsonify(data = user_dict, status = {'code': 200, 'message': 'User successfully logged in!'}), 200
        else:
            return jsonify(data = {}, status = {'code': 401, 'message': 'Username or password did not match!'}), 401
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 401, 'message': 'Username or password did not match!'}), 401

# CHECK LOGGED IN USER
@users.route('/logged_in_user', methods = ['GET'])
def get_logged_in_user():
    print(current_user)
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')
    return jsonify(
        data = user_dict
        ), 200

# LOGOUT ROUTE
@users.route('/logout', methods = ['GET'])
def logout():
    logout_user()
    return jsonify(
        data = {},
        message = 'Successfully logged out.',
        status = 200
    ), 200

# SHOW USERS ROUTE
@users.route('/', methods = ['GET'])
def get_users():
    user_dicts = [model_to_dict(user) for user in models.User]
    for user in user_dicts:
        user.pop('password')
    return jsonify({
        'data': user_dicts,
        'message': f'Successfully found {len(user_dicts)} users.',
        'status': 200
    }), 200

# SHOW A USERS STAX ROUTE
@users.route('/<user>/records', methods = ['GET'])
def get_users_records(user):
    user_int = int(user)
    user_records_dicts = [model_to_dict(record) for record in models.Record if record.owner.id == user_int]
    for record in user_records_dicts:
        record['owner'].pop('password')
    return jsonify({
        'data': user_records_dicts,
        'message': f'Successfully found {len(user_records_dicts)} records.',
        'status': 200
    }),200
