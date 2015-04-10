# coding: utf-8
from pymongo import MongoClient
from flask import Flask, render_template, abort, request, url_for, redirect, request, jsonify, flash, session, g, json
from bson.json_util import dumps
from werkzeug import check_password_hash, generate_password_hash
from bson.objectid import ObjectId

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
    _objects = objects.find()
    return render_template('index.html', show_tags=[tag['name'] for tag in _tags], show_objects=[obj['name'] for obj in _objects])

@app.route("/objects/")
@app.route("/tags/")
def gotohome():
    return redirect('/')

#_____Collection
@app.route('/collection')
def collection():
    if 'username' not in session:
        flash('Log in, please')
        return redirect('/login')

    # берём айди тегов юзера
    my_tags_id = [my_tag_id['_id'] for my_tag_id in g.user['tags']]
    print my_tags_id
    print [i['name'] for i in db.tags.find({'_id':{'$in': my_tags_id}})]
    # и выводим в шаблон их имена
    return render_template('collection.html', show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': my_tags_id}})])

#_____Collection/
#_____Tags

@app.route('/<tag>')
def unknown_tag(tag):
    return render_template('404.html', show_name=tag)

@app.route('/tags/<tag>', methods=['GET', 'POST'])
def tag_page(tag):
    """Tag page and tag adding to collection"""
    current_tag = tags.find_one({'name': tag})

    # проверяем залогиненность что бы взять теги из юзера
    if g.user:
        user_tags = [user_tag['_id'] for user_tag in g.user['tags']]
    if request.method == 'POST':
        # print current_tag["_id"]
        # print user_tags
        if current_tag["_id"] not in user_tags:
            db.users.update({"username":session["username"]}, 
                 {'$push': { 
                            "tags":{ "_id": current_tag['_id'] } 
                          }
                 }
                 )

        else:
            db.users.update({"username":session["username"]}, 
                 {'$pull': { 
                            "tags":{ "_id": current_tag['_id'] } 
                          }
                 }
                 )

    if current_tag:
        if g.user and current_tag['_id'] in user_tags:
            # проверяем есть ли тег в коллекции у юзера
            return render_template('tag.html', description=current_tag['description'], name=current_tag['name'], id=current_tag['_id'], myTag=True)
        return render_template('tag.html', description=current_tag['description'], name=current_tag['name'], id=current_tag['_id'])
    else:
        return render_template('404.html', show_name=tag)

@app.route('/tags/add')
def add_tag_page():
    name = request.args.get('name')
    if 'username' not in session:
        flash('Log in, please')
        return redirect('/login')
    if name == None:
        name = ''
    return render_template('add_tag.html', tag_name=name)

@app.route('/api/tags/<name>', methods=['GET', 'PUT', 'DELETE'])
def get_tag(name):
    if request.method == 'GET':
        current_tag = tags.find_one({'name': name})
        return dumps(current_tag)
    if request.method == 'PUT':
        tags.update({'name': name}, {'name': name})
    if request.method == 'DELETE':
        tags.remove({'name': name}, {justOne: true})

@app.route('/api/add/tag', methods=['POST'])
def add_tag():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        _id = tags.insert({'name': name, 'description': description})
        db.users.update({"username":session["username"]}, 
                 {'$push': { 
                            "tags":{ "_id": _id } 
                          }
                 }
                 )
        response = jsonify(message=str('OK'))
        response.status_code = 200
        return response

#_____Tags/
#_____Objects

@app.route('/objects/<obj>', methods=['GET', 'POST'])
def obj_page(obj):
    """Object page"""
    current_object = objects.find_one({'name': obj})

    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        print data['value']
        db.objects.update({"name":obj}, 
                 {'$push': { 
                            "tags":{ "_id": ObjectId(data['value'])} 
                          }
                 }
                 )

    # берём айди тегов объекта
    object_tags_id = [my_tag_id['_id'] for my_tag_id in current_object['tags']]
    # print object_tags_id
    # print [i['name'] for i in db.tags.find({'_id':{'$in': object_tags_id}})]

    # проверяем залогиненность, что бы взять теги у юзера для вывода в список
    if g.user:
        my_tags_id = [my_tag_id['_id'] for my_tag_id in g.user['tags']]
        my_tags_name = [i for i in db.tags.find({'_id':{'$in': my_tags_id}})]
    else:
        my_tags_name = []
    # и выводим в шаблон их имена
    return render_template(
        'object.html',
        show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': object_tags_id}})],
        name=current_object['name'],
        description=current_object['description'],
        id=current_object['_id'],
        user_tags=my_tags_name
    )

#_____Objects/
#_____Auth
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
            users.insert({'username': username, 'email': email, 'password': password, 'tags': []})
            flash('Welcome to Boojom, ' + username)
            return redirect('/login')
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
#_____Auth/


"""
не пашит :-(
if app.debug:
    from flaskext.stylus2css import stylus2css
    stylus2css(app, css_folder='static/css', stylus_folder='stylus')
"""
