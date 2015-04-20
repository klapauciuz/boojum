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

@app.route("/howtouse")
def info():
    return render_template('info.html')

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
    # берём айди объектов юзера
    my_objs_id = [my_obj_id['_id'] for my_obj_id in g.user['objects']]
    print my_objs_id
    print [i['name'] for i in db.objects.find({'_id':{'$in': my_objs_id}})]

    # и выводим в шаблон их имена
    return render_template('collection.html', show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': my_tags_id}})], show_objects=[i['name'] for i in db.objects.find({'_id':{'$in': my_objs_id}})])

#_____Collection/
#_____Tags

@app.route('/<tag>')
def unknown_tag(tag):
    """Unknown tag redirect"""
    return render_template('404.html', show_name=tag)

@app.route('/tags/<tag>', methods=['GET', 'POST', 'DELETE'])
def tag_page(tag):
    """Tag page and tag adding to collection"""
    current_tag = tags.find_one({'name': tag})

    # проверяем залогиненность что бы взять теги из юзера
    if g.user:
        user_tags = [user_tag['_id'] for user_tag in g.user['tags']]
    if request.method == 'DELETE':
        tags.remove({'_id': current_tag['_id']})
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

    # находим создателя тега
    creator = db.users.find_one({'_id': current_tag['creator']})
    # берём айди объектов тега
    tags_objects_id = [my_obj_id['_id'] for my_obj_id in current_tag['objects']]
    if current_tag:
        if g.user and current_tag['_id'] in user_tags:
            # проверяем есть ли тег в коллекции у юзера
            return render_template('tag.html', show_objects=[i['name'] for i in db.objects.find({'_id':{'$in': tags_objects_id}})], description=current_tag['description'], name=current_tag['name'], id=current_tag['_id'], creator=creator['username'], myTag=True)
        return render_template('tag.html', show_objects=[i['name'] for i in db.objects.find({'_id':{'$in': tags_objects_id}})], description=current_tag['description'], name=current_tag['name'], id=current_tag['_id'], creator=creator['username'])
    else:
        return render_template('404.html', show_name=tag)

@app.route('/tags/add', methods=['GET', 'POST'])
def add_tag_page():
    """New tag page/add"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        linked_objects = []
        creator = g.user['_id']
        # если есть строка с объектами то берём её и обрезаем, попутно удаляя ненужные пробелы вначале
        # if request.form['objects']:
        #     objects = [obj.lstrip() for obj in request.form['objects'].split(',')]
        # else:
        #     objects = []
        # в форме добавления нового тега должен быть динамический выпадающий список объектов, вводим А - выпадают все объекты на А и т.д.
        # сейчас связанные теги к объектам добавляются только через роут объекта(когда прикрепляем к нему тег)
        _id = tags.insert({'name': name, 'description': description, 'objects': linked_objects, 'creator': creator})
        db.users.update({"username":session["username"]}, 
                 {'$push': { 
                            "tags":{ "_id": _id } 
                          }
                 }
                 )
        response = jsonify(message=str('OK'))
        response.status_code = 200
        return response

    name = request.args.get('name')
    if 'username' not in session:
        flash('Log in, please')
        return redirect('/login')
    if name == None:
        name = ''
    _objects = objects.find()
    return render_template('add_tag.html', tag_name=name, show_objects=[obj['name'] for obj in _objects])

# немного сократили код )
# @app.route('/api/add/tag', methods=['POST'])
# def add_tag():
#     """Add new tag"""
#     if request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']

#         # если есть строка с объектами то берём её и обрезаем, попутно удаляя ненужные пробелы вначале
#         # if request.form['objects']:
#         #     objects = [obj.lstrip() for obj in request.form['objects'].split(',')]
#         # else:
#         #     objects = []
#         objects = []
#         # в форме добавления нового тега должен быть динамический выпадающий список объектов, вводим А - выпадают все объекты на А и т.д.
#         # сейчас связанные теги к объектам добавляются только через роут объекта(когда прикрепляем к нему тег)
#         _id = tags.insert({'name': name, 'description': description, 'objects': objects})
#         db.users.update({"username":session["username"]}, 
#                  {'$push': { 
#                             "tags":{ "_id": _id } 
#                           }
#                  }
#                  )
#         response = jsonify(message=str('OK'))
#         response.status_code = 200
#         return response

# так и не понял что это и зачем
# @app.route('/api/tags/<name>', methods=['GET', 'PUT', 'DELETE'])
# def get_tag(name):
#     if request.method == 'GET':
#         current_tag = tags.find_one({'name': name})
#         return dumps(current_tag)
#     if request.method == 'PUT':
#         tags.update({'name': name}, {'name': name})
#     if request.method == 'DELETE':
#         tags.remove({'name': name}, {justOne: true})
#_____Tags/
#_____Objects

# @app.route('/collection/add/<obj>', methods=['GET', 'POST'])
# def add_object(obj):
#     """Object add"""
#     current_object = objects.find_one({'name': obj})
#     if g.user:
#         user_objects = [user_obj['_id'] for user_obj in g.user['objects']]
        
#     if request.method == 'POST':
#         # print current_object["_id"]
#         # print user_tags


#     response = jsonify(message=str('OK'))
#     response.status_code = 200
#     return response

@app.route('/objects/<obj>', methods=['GET', 'POST'])
def obj_page(obj):
    """Object page and add object to collection"""
    current_object = objects.find_one({'name': obj})
    if g.user:
        user_objects = [user_obj['_id'] for user_obj in g.user['objects']]

    if request.method == 'POST':
        # если прикрепляем тег к объекту
        if request.form.get('data'):
            data = json.loads(request.form.get('data'))
            print data['value']
            print data['name']
            db.objects.update({"name":obj}, 
                     {'$push': { 
                                "tags":{ "_id": ObjectId(data['value'])} 
                              }
                     }
                     )

            # добавляем объект в тег (для отображения объектов, у которых есть данный тег)
            db.tags.update({"_id":ObjectId(data['value'])}, 
                     {'$push': { 
                                "objects":{ "_id": current_object['_id']} 
                              }
                     }
                     )
            response = jsonify(message=str('OK'))
            response.status_code = 200
            return response

        # если добавляем объект в коллекцию
        else:
            if current_object["_id"] not in user_objects:
                db.users.update({"username":session["username"]}, 
                     {'$push': { 
                                "objects":{ "_id": current_object['_id'] } 
                              }
                     }
                     )

            else:
                db.users.update({"username":session["username"]}, 
                     {'$pull': { 
                                "objects":{ "_id": current_object['_id'] } 
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
    if g.user and current_object['_id'] in user_objects:
        return render_template(
            'object.html',
            show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': object_tags_id}})],
            name=current_object['name'],
            description=current_object['description'],
            id=current_object['_id'],
            user_tags=my_tags_name,
            myObj = True
        )
    else:
        return render_template(
            'object.html',
            show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': object_tags_id}})],
            name=current_object['name'],
            description=current_object['description'],
            id=current_object['_id'],
            user_tags=my_tags_name
        )

#_____Objects/
#_____Fill

#_____Fill/
#_____User
@app.route('/users/<user>')
def user(user):
    if 'username' in session:
        if user == g.user['username']:
            return redirect('/collection')

    current_user = users.find_one({'username': user})

    # берём айди объектов юзера
    user_objects_id = [user_obj_id['_id'] for user_obj_id in current_user['objects']]
    # берём айди тегов юзера
    user_tags_id = [user_tag_id['_id'] for user_tag_id in current_user['tags']]

    if 'username' in session:
        # берём айди своих тегов
        my_tags_id = [my_tag_id['_id'] for my_tag_id in g.user['tags']]
        # берём айди своих объектов
        my_objs_id = [my_obj_id['_id'] for my_obj_id in g.user['objects']]
        # ищем общие теги
        mu_tags_id = [i for i in my_tags_id if i in user_tags_id]
        print mu_tags_id
        # и объекты
        mu_objects_id = [i for i in my_objs_id if i in user_objects_id]
        print mu_objects_id
        # создаём список из их имён
        mu_tags_names = [i['name'] for i in db.tags.find({'_id':{'$in': mu_tags_id}})]
        mu_objs_names = [i['name'] for i in db.objects.find({'_id':{'$in': mu_objects_id}})]
    else:
        mu_tags_names = []
        mu_objs_names = []

    return render_template('user.html', user_name=user, show_mu_tags=mu_tags_names, show_mu_objects=mu_objs_names, show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': user_tags_id}})], show_objects=[i['name'] for i in db.objects.find({'_id':{'$in': user_objects_id}})])


#_____User/
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
            users.insert({'username': username, 'email': email, 'password': password, 'tags': [], 'objects': []})
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
