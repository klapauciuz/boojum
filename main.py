# coding: utf-8
from pymongo import MongoClient
from flask import Flask, render_template, abort, request, url_for, redirect, request, jsonify, flash, session, g, json
from bson.json_util import dumps
from werkzeug import check_password_hash, generate_password_hash, secure_filename
from bson.objectid import ObjectId
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client['boojom']
tags = db.tags
objects = db.objects
users = db.users

UPLOAD_FOLDER = 'static\\images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = users.find_one({'username': session['username']})

@app.route("/")
def hello():
    _tags = tags.find()
    _objects = objects.find()
    _users = users.find()
    return render_template('index.html', show_people=[user['username'] for user in _users], show_tags=[tag['name'] for tag in _tags], show_objects=[obj['name'] for obj in _objects])

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

    # берём айди своих тегов
    my_tags_id = [my_tag_id['_id'] for my_tag_id in g.user['tags']]
    print my_tags_id
    print [i['name'] for i in db.tags.find({'_id':{'$in': my_tags_id}})]
    # берём айди своих объектов
    my_objs_id = [my_obj_id['_id'] for my_obj_id in g.user['objects']]
    print my_objs_id
    print [i['name'] for i in db.objects.find({'_id':{'$in': my_objs_id}})]
    # берём айди своих друзей
    my_flws_id = [my_flw_id['_id'] for my_flw_id in g.user['friends']]
    print my_flws_id
    print 'my friends:', [i['username'] for i in db.users.find({'_id':{'$in': my_flws_id}})]
    # и выводим в шаблон их имена
    return render_template('collection.html', show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': my_tags_id}})], show_objects=[i['name'] for i in db.objects.find({'_id':{'$in': my_objs_id}})], show_friends=[i['username'] for i in db.users.find({'_id':{'$in': my_flws_id}})])

#_____Collection/
#_____Fill
@app.route('/collection/<TO>/fill', methods=['GET', 'POST'])
def fill(TO):
    if g.user:
        user_tags = [user_tag['_id'] for user_tag in g.user['tags']]
        user_objs = [user_tag['_id'] for user_obj in g.user['objects']]
    # берём айди тегов юзера
    my_tags_id = [my_tag_id['_id'] for my_tag_id in g.user['tags']]
    # берём айди объектов юзера
    my_objs_id = [my_obj_id['_id'] for my_obj_id in g.user['objects']]
    if TO == 'tags':
        # ищем все теги у объектов юзера
        for my_obj_tag in objects.find({'_id':{'$in': my_objs_id}}):
            for tag in my_obj_tag['tags']:
                if tag['_id'] not in user_tags:
                    db.users.update({"username":session["username"]}, 
                         {'$push': { 
                                    "tags":{ "_id": tag['_id'] } 
                                  }
                         }
                         )
        response = jsonify(message=str('OK'))
        response.status_code = 200
        return response
    else:
        # ищем все теги у объектов юзера
        for my_tag_obj in tags.find({'_id':{'$in': my_tags_id}}):
            for obj in my_tag_obj['objects']:
                if obj['_id'] not in user_objs:
                    db.users.update({"username":session["username"]}, 
                         {'$push': { 
                                    "objects":{ "_id": obj['_id'] } 
                                  }
                         }
                         )
        response = jsonify(message=str('OK'))
        response.status_code = 200
        return response

#_____Fill/

#_____Files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print request.form['id']
            db.objects.update({"_id":ObjectId(request.form['id'])}, 
                         {'$push': { 
                                    "images": filename
                                  }
                         }
                         )
            response = jsonify(message=str('OK'))
            response.status_code = 200
            return response
    return redirect('/')
#_____Files/

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

    show_objects = [i for i in db.objects.find({'_id':{'$in': tags_objects_id}})]
    if current_tag:
        if g.user and current_tag['_id'] in user_tags:
            # проверяем есть ли тег в коллекции у юзера
            return render_template('tag.html', show_objects=show_objects, description=current_tag['description'], name=current_tag['name'], id=current_tag['_id'], creator=creator['username'], myTag=True)
        return render_template('tag.html', show_objects=show_objects, description=current_tag['description'], name=current_tag['name'], id=current_tag['_id'], creator=creator['username'])
    else:
        return render_template('404.html', show_name=tag)

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
            values = data['values']
            names = data['names'].split(', ')
            for x in xrange(0, len(values)):
                print names[x], ':', values[x]
                db.objects.update({"name": obj}, 
                         {'$push': { 
                                    "tags":{ "_id": ObjectId(values[x])} 
                                  }
                         }
                         )

                # добавляем объект в тег (для отображения объектов, у которых есть данный тег)
                db.tags.update({"_id":ObjectId(values[x])}, 
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
            source=current_object['source'],
            user_tags=my_tags_name,
            myObj = True,
            images=current_object['images']
        )
    else:
        return render_template(
            'object.html',
            show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': object_tags_id}})],
            name=current_object['name'],
            description=current_object['description'],
            id=current_object['_id'],
            source=current_object['source'],
            user_tags=my_tags_name,
            images=current_object['images']
        )

#_____Objects/

@app.route('/objects/add', methods=['POST'])
def add_object_from_wiki():
    """New object add"""
    try:
        if request.form['urlwiki'] == '':
            print 'fromlastfm, url:', request.form['urllast']
            r = requests.get(request.form['urllast'])
            soup = BeautifulSoup(r.text)
            name = re.sub(r'[\ \n]{2,}', '', soup.find("article", class_='artist-overview').find('h1').text)
            description = soup.find('div', class_='wiki-text').text
            source = request.form['urllast']
            print name
        else:
            print 'fromwiki, url:', request.form['urlwiki']
            r = requests.get(request.form['urlwiki'])
            soup = BeautifulSoup(r.text)
            name = soup.find("h1", class_="firstHeading").text
            descriptions = soup.find("div", id='mw-content-text').find_all("p", recursive=False)
            description = descriptions[0].text
            source = request.form['urlwiki']
    except:
        flash('Wrong URL')
        return '/tags/add'
    if db.objects.find({'name': re.sub(r'(\n|\t)', '', name)}).limit(1).count() > 0:
        response = '/objects/' + re.sub(r'(\n|\t)', '', name)
        return response
    _id = objects.insert({'name': re.sub(r'(\n|\t)', '', name), 'description': description, 'images': [], 'tags': [], 'source': source})
    db.users.update({"username":session["username"]}, 
         {'$push': { 
                    "objects":{ "_id": _id } 
                  }
         }
         )
    response = '/objects/' + re.sub(r'(\n|\t)', '', name)
    thanks_string = 'Done. Thank you for another new object, ' + session["username"]
    flash(thanks_string)
    return response

    # with open('wiki.html', 'w') as wiki:
    #     wiki.write(r.text.encode('utf-8'))

    # response = jsonify(message=str('OK'))
    # response.status_code = 200
    # return response

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
        response = name
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

#_____User
@app.route('/users/<user>', methods=['GET', 'POST', 'DELETE'])
def user(user):
    if 'username' in session:
        if user == g.user['username']:
            return redirect('/collection')

    current_user = users.find_one({'username': user})
    user_friends = [user_fri_id['_id'] for user_fri_id in current_user['friends']]
    print 'user friends:', [ObjectId(str(x)) for x in user_friends]
    user_friends_names = [friend['username'] for friend in db.users.find({'_id':{'$in': user_friends}})]
    # if request.method == 'DELETE':
    #     users.remove({'_id': current_user['_id']})

    if request.method == 'POST':
        db.users.update({"username":session["username"]}, 
             {'$push': { 
                        "friends":{ "_id": current_user['_id'] } 
                      }
             }
             )
        db.users.update({"username":user}, 
             {'$push': { 
                        "friends":{ "_id": g.user['_id'] } 
                      }
             }
             )
    if request.method == 'DELETE':
        db.users.update({"username":session["username"]}, 
             {'$pull': { 
                        "friends":{ "_id": current_user['_id'] } 
                      }
             }
             )
        db.users.update({"username":user}, 
             {'$pull': { 
                        "friends":{ "_id": g.user['_id'] } 
                      }
             }
             )
    # берём айди объектов юзера
    user_objects_id = [user_obj_id['_id'] for user_obj_id in current_user['objects']]
    # берём айди тегов юзера
    user_tags_id = [user_tag_id['_id'] for user_tag_id in current_user['tags']]
    # берём айди друзей юзера
    user_flws_id = [user_flw_id['_id'] for user_flw_id in current_user['friends']]
    print user_flws_id
    print 'user friends:', [i['username'] for i in db.users.find({'_id':{'$in': user_flws_id}})]

    if 'username' in session:
        # берём айди своих тегов
        my_tags_id = [my_tag_id['_id'] for my_tag_id in g.user['tags']]
        # берём айди своих объектов
        my_objs_id = [my_obj_id['_id'] for my_obj_id in g.user['objects']]
        # ищем общие теги
        mu_tags_id = [i for i in my_tags_id if i in user_tags_id]
        print 'mutual tags id:', mu_tags_id
        # и объекты
        mu_objects_id = [i for i in my_objs_id if i in user_objects_id]
        print 'mutual objects id:', mu_objects_id
        # создаём список из их имён
        mu_tags_names = [i['name'] for i in db.tags.find({'_id':{'$in': mu_tags_id}})]
        mu_objs_names = [i['name'] for i in db.objects.find({'_id':{'$in': mu_objects_id}})]
    else:
        mu_tags_names = []
        mu_objs_names = []

    if 'username' in session:
        if g.user['_id'] not in user_friends:
            return render_template('user.html', show_friends=[i['username'] for i in db.users.find({'_id':{'$in': user_flws_id}})], user_name=user, show_mu_tags=mu_tags_names, show_mu_objects=mu_objs_names, show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': user_tags_id}})], show_objects=[i['name'] for i in db.objects.find({'_id':{'$in': user_objects_id}})])
        else:
            return render_template('user.html', Friend=True, show_friends=[i['username'] for i in db.users.find({'_id':{'$in': user_flws_id}})], user_name=user, show_mu_tags=mu_tags_names, show_mu_objects=mu_objs_names, show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': user_tags_id}})], show_objects=[i['name'] for i in db.objects.find({'_id':{'$in': user_objects_id}})])
    else:
        return render_template('user.html', show_friends=[i['username'] for i in db.users.find({'_id':{'$in': user_flws_id}})], user_name=user, show_mu_tags=mu_tags_names, show_mu_objects=mu_objs_names, show_tags=[i['name'] for i in db.tags.find({'_id':{'$in': user_tags_id}})], show_objects=[i['name'] for i in db.objects.find({'_id':{'$in': user_objects_id}})])
#_____User/
#_____Auth
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        flash('You are already registered in Boojum, ' + session['username'])
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
            users.insert({'username': username, 'email': email, 'password': password, 'tags': [], 'objects': [], 'friends': []})
            flash('Welcome to Boojum, ' + username)
            return redirect('/login')
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('You are already in Boojum, ' + session['username'])
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
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)
#_____Auth/


"""
не пашит :-(
if app.debug:
    from flaskext.stylus2css import stylus2css
    stylus2css(app, css_folder='static/css', stylus_folder='stylus')
"""
