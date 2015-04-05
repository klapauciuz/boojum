import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, abort, json, jsonify
import json
from bson import json_util

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client['boojom']
tags = db['tags']
objects = db['objects']


@app.route("/")
def hello():
    return render_template('index.html', show_tags=[tag['name'] for tag in tags.find()], show_objects=[obj['name'] for obj in objects.find()])

@app.route('/<tag>')
def tag_page(tag):
    _tag = tags.find_one({'name': tag})
    if _tag:
        return render_template('tag.html', show_name=_tag['name'])
    else:
        return render_template('404.html', show_name=tag)

@app.route('/api/tag/<id>')
def get_tag(id):
    return jsonify(
        name=id
    )
def output_json(obj, code, headers=None):
    """
    This is needed because we need to use a custom JSON converter
    that knows how to translate MongoDB types to JSON.
    """
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})

    return resp

@app.route('/api/tags')
def tags_list():
    if request.method == 'GET':
#        limit = int(request.args.get('limit', 10))
#        offset = int(request.args.get('offset', 0))
        json_results = []
        json_docs = [json.dumps(doc, default=json_util.default) for doc in tags.find()]
        return str(json_docs)


if __name__ == "__main__":
    app.run()
