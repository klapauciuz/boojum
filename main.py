import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, abort
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
    tags_list = [i_tag['name'] for i_tag in tags.find()]
    if tag not in tags_list:
    	return render_template('404.html', show_name=tag)
    return render_template('tag.html', show_name=tag)

if __name__ == "__main__":
    app.run()
