# coding: utf-8
from pymongo import MongoClient
from flask import Flask, render_template, abort, request, url_for, redirect, request, jsonify, flash, session, g
from bson.json_util import dumps
from werkzeug import check_password_hash, generate_password_hash

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client['boojom']
tags = db.tags
objects = db.objects
users = db.users

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = users.find_one({'username': session['username']})

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
    if 'username' not in session:
        flash('Log in, please')
        return redirect('/login')
    if name == None:
        name = ''
    return render_template('add_tag.html', tag_name=name)


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


@app.route('/api/add/tag', methods=['POST'])
def add_tag():
    if request.method == 'POST':
        app.logger.info('name is: %s', request.form)
        name = request.form['name']
        tags.insert({'name': name})
        response = jsonify(message=str('OK'))
        response.status_code = 200
        return response

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        flash('You are already registered in Boojom, ' + session['username'])
        return redirect('/')
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        else:
            username = request.form['username']
            email = request.form['username']
            password = generate_password_hash(request.form['password'])
            users.insert({'username': username, 'email': email, 'password': password})
            flash('Welcome to Boojom, ' + username)
            return redirect('/login')
    if request.method == 'GET':
        return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('You are already in Boojom, ' + session['username'])
        return redirect('/')
    error = None
    if request.method == 'POST':
        user = users.find_one({'username': request.form['username']})
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['password'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('Nice to see you again, ' + user['username'])
            session['username'] = user['username']
            return redirect('/')
    if request.method == 'GET':
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    flash('Bye bye, ' + session['username'])
    session.pop('username', None)
    return redirect('/')

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)

"""
не пашит :-(
if app.debug:
    from flaskext.stylus2css import stylus2css
    stylus2css(app, css_folder='static/css', stylus_folder='stylus')
"""
