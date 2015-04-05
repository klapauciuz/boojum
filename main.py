# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, abort, json, jsonify
import json
from bson import Binary, Code
from bson.json_util import dumps

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
    resp = dumps(tags.find())
    return resp

@app.route('/api/tags/<name>')
def get_tag(name):
    current_tag = tags.find_one({'name': name})
    return dumps(current_tag)

if __name__ == "__main__":
    app.run(debug=True)
