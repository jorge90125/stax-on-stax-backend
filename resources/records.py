from email import message
import json
import models
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

records = Blueprint('records', 'records')

# SHOW RECORDS ROUTE
@records.route('/', methods = ['GET'])
def records_index():
    result = models.Record.select()
    current_user_record_dicts = [model_to_dict(record) for record in current_user.records]
    for record_dict in current_user_record_dicts:
        record_dict['owner'].pop('password')
    return jsonify({
        'data': current_user_record_dicts,
        'message': f'Successfully fount {len(current_user_record_dicts)} records',
        'status': 200
    }), 200

# RECORD CREATE ROUTE
@records.route('/', methods = ['POST'])
def create_records():
    payload = request.get_json()
    new_record = models.Record.create(name = payload['name'], artist = payload['artist'], artwork_url = payload['artwork_url'], release_year = payload['release_year'], pressing_year = payload['pressing_year'], genre = payload['genre'], record_label = payload['record_label'], catalog_num = payload['catalog_num'], country = payload['country'], owner = current_user.id)
    record_dict = model_to_dict(new_record)
    record_dict['owner'].pop('password')
    return jsonify(
        data = record_dict,
        message = 'Successfully created record',
        status = 201
    ), 201