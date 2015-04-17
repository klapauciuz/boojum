from flask import Flask
from flask.ext.mongoengine import MongoEngine
from mongoengine import connect

app = Flask(__name__)

# look at http://flask.pocoo.org/docs/0.10/patterns/appdispatch/ to make host like boojum.boo
# app.config['SERVER_NAME'] = 'boojum.boo:5000'

app.config["MONGODB_SETTINGS"] = {
    'DB': "boojom",
    'host': 'localhost:27017'
}
app.config["SECRET_KEY"] = "super secret key"

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()