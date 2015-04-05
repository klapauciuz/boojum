# coding: utf-8
from pymongo import MongoClient
from flask import Flask, render_template, abort, request, url_for
from urlparse import urlparse, urljoin
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

@app.route('/<tag>/add')
def add_tag_page(tag):
    return render_template('add_tag.html', tag_name=tag)

"""
 получить коллекцию тегов в JSON,
 У роута должно быть два параметра limit и offset, для слайса выборки
 TODO:
 стоит сменить url для API на
 'api/tags' - метод GET и POST (чтобы можно было туда оправлить новый тег),
 'api/tags/<id>' - методы GET, PUT, DELETE для работы с конкретным тегом
"""
@app.route('/api/tags/',  methods=['GET'])
def tags_list():
    resp = dumps(tags.find())
    return resp

@app.route('/api/tags/<name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_tag(name):
    if request.method == 'GET':
        current_tag = tags.find_one({'name': name})
        return dumps(current_tag)
    #TODO: refact, возможно для добавления лучше url без переменной /api/tags/add
    if request.method == 'POST':
        # почему-то после отправки стандартным способом не показывает тег, но если снова зайти на страницу то ОК - видно JSON
        tags.insert({'name': name})
    if request.method == 'PUT':
        tags.update({'name': name}, {'name': name})
    if request.method == 'DELETE':
        tags.remove({'name': name}, {justOne: true})


if __name__ == "__main__":
    app.run(debug=True)
