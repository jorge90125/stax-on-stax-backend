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
    new_record = models.Record.create(
        name = payload['name'],
        artist = payload['artist'],
        artwork_url = payload['artwork_url'],
        release_year = payload['release_year'],
        pressing_year = payload['pressing_year'],
        genre = payload['genre'],
        record_label = payload['record_label'],
        catalog_num = payload['catalog_num'],
        country = payload['country'],
        owner = current_user.id
    )
    record_dict = model_to_dict(new_record)
    record_dict['owner'].pop('password')
    return jsonify(
        data = record_dict,
        message = 'Successfully created record',
        status = 201
    ), 201

# ALL TOGETHER ROUTE
@records.route('/<id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_one_record(id):
    if request.method == 'GET':
        record = models.Record.get_by_id(id)
        # print(record)
        data = model_to_dict(record)
        data['owner'].pop('password')
        return jsonify(
            data = data,
            message = 'Successfully showing record!',
            status = 200
        ), 200
    payload = request.get_json() if request.method == 'PUT' else None
    query = models.Record.update(**payload).where(models.Record.id == id) if payload else models.Record.delete().where(models.Record.id == id)
    query.execute()
    data = model_to_dict(models.Record.get_by_id(id)) if request.method == 'PUT' else [model_to_dict(record) for record in models.Record.select()]
    if request.method == 'DELETE':
        for record in data:
            record['owner'].pop('password')
    return jsonify(
        data = data,
        message = 'Record updated successfully!' if payload else 'Record successfully deleted!',
        status = 200
    ), 200