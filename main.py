import pymongo
from pymongo import MongoClient
from flask import Flask, render_template
app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client['boojom']
tags = db['tags']
objects = db['objects']


@app.route("/")
def hello():
    return render_template('index.html', show_tags=[tag['name'] for tag in tags.find()], show_objects=[obj['name'] for obj in objects.find()])

@app.route('/api/<test>')
def tags():
#    app.logger.debug('name is %d', test)
    response.status_code(500)
    response.data(test)
    return 'test %d' % test


if __name__ == "__main__":
    app.run()
