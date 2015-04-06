# coding: utf-8
from pymongo import MongoClient
from flask import Flask, render_template, abort, request, url_for, redirect, request, jsonify
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client['boojom']
tags = db.tags
objects = db.objects


@app.route("/")
def hello():
    _tags = tags.find()
    return render_template('index.html', show_tags=[tag['name'] for tag in _tags], show_objects=[obj['name'] for obj in objects.find()])

@app.route('/<tag>')
def tag_page(tag):
    current_tag = tags.find_one({'name': tag})
    if current_tag:
        return render_template('tag.html', name=current_tag['name'], id=current_tag['_id'])
    else:
        return render_template('404.html', show_name=tag)

@app.route('/tag/add')
def add_tag_page():
    name = request.args.get('name')
    #OMG_))
    if name == None:
        name = ''
    return render_template('add_tag.html', tag_name=name)

"""
 получить коллекцию тегов в JSON,
 У роута должно быть два параметра limit и offset, для слайса выборки
 TODO:
 стоит сменить url для API на
 'api/tags' - метод GET и POST (чтобы можно было туда оправлить новый тег),
 'api/tags/<name>' - методы GET, PUT, DELETE для работы с конкретным тегом
"""

@app.route('/api/tags/',  methods=['GET'])
def tags_list():
    resp = dumps(tags.find())
    return resp

@app.route('/api/tags/<name>', methods=['GET', 'PUT', 'DELETE'])
def get_tag(name):
    if request.method == 'GET':
        current_tag = tags.find_one({'name': name})
        app.logger.info('params are: %s', request.url)
        return dumps(current_tag)
    if request.method == 'PUT':
        tags.update({'name': name}, {'name': name})
    if request.method == 'DELETE':
        tags.remove({'name': name}, {justOne: true})
    '''
    возможно понадобиться
    if request.method == 'POST':
        # почему-то после отправки стандартным способом не показывает тег, но если снова зайти на страницу то ОК - видно JSON
        tags.insert({'name': name})
        # https://gist.github.com/ibeex/3257877
        app.logger.info('params are: %s', request.query_string)
        return redirect('/'+name)
    '''


@app.route('/api/add/tag', methods=['POST'])
def add_tag():
    if request.method == 'POST':
        app.logger.info('name is: %s', request.form)
        name = request.form['name']
        tags.insert({'name': name})
        # return redirect('/'+name)
        # return tags.find_one({'name': name})
        response = jsonify(message=str('ЗБС'))
        response.status_code = 200
        return response


if __name__ == "__main__":
    app.run(debug=True)
