# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, abort, json, jsonify
import json
from bson import json_util, ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client['boojom']
tags = db['tags']
objects = db['objects']


# конвертер в JSON - не работает
def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

@app.route("/")
def hello():
    return render_template('index.html', show_tags=[tag['name'] for tag in tags.find()], show_objects=[obj['name'] for obj in objects.find()])

@app.route('/<tag>')
def tag_page(tag):
    current_tag = tags.find_one({'name': tag})
    if current_tag:
        return render_template('tag.html', name=current_tag['name'], id=current_tag['_id'])
    else:
        return render_template('404.html', show_name=tag)

# просто тест переменной роута и выдачей JSON
@app.route('/api/tags/<id>')
def get_tag(id):
    current_tag = tags.find_one({'name': id})
    return jsonify(
        name=id
    )

"""
 получить коллекцию тегов в JSON,
 У роута должно быть два параметра limit и offset, для слайса выборки
 TODO:
 стоит сменить url для API на
 'api/tags' - метод GET и POST (чтобы можно было туда оправлить новый тег),
 'api/tags/<id>' - методы GET, PUT, DELETE для работы с конкретным тегом
"""
@app.route('/api/tags/')
def tags_list():
    course_list = list( objects.find() )
    resp = jsonify({'tags-collection': [
        {'_id': 'OBJ', 'name': 'WTF'},
        {'_id': 'OBJ', 'name': 'WTF'},
        {'_id': 'OBJ', 'name': 'WTF'},
        {'_id': 'OBJ', 'name': 'WTF'},
        {'_id': 'OBJ', 'name': 'WTF'},
        {'_id': 'OBJ', 'name': 'WTF'}
    ]})
    resp.status_code = 200
    return resp
#       limit = int(request.args.get('limit', 10))
#       offset = int(request.args.get('offset', 0))
#        json_results = []



if __name__ == "__main__":
    app.run(debug=True)
