import sqlite3
import sys

import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session
from itsdangerous import json





# База данных
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    users = db.Column(db.String(30), nullable=False)







#Основыне константы
baseURL = 'http://127.0.0.1:'
urlPosts = baseURL + '8002/posts/'
urlLike = baseURL + '8000/likes/'
urlComment = baseURL + '8001/comments/'
app.config['SECRET_KEY'] = 'cb02820a3e94d72c9f950ee10ef7e3f7a35b3f5b'







# Аунтификация


# Страница аунтификации
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        index = int(request.form['index'])
        if index==1:
            name = request.form['name']
            password = request.form['password']
            authorized = auth(name, password)
            if authorized:
                posts = requests.get(urlPosts).content
                array = json.loads(posts)
                array.sort(key=sortId, reverse=True)
                userId = getIdFromName(name)
                return render_template('chat.html', data=array, userId=userId)
            else:
                return render_template('/index.html')
        return chat()
    elif request.method == "GET":
        return render_template('/index.html')
    else:
        return "Вы пытаетесь совершить незапланиуремую операцию"


#Проверка пользователя
def auth(name, password):
    session['name'] = name
    correct_password = getPasswordFromName(name)
    if not correct_password:
        item = Item(name=name, password=password, users="user")
        db.session.add(item)
        db.session.commit()
        return True
    elif correct_password == password:
        return True
    else:
        return False









#Посты

def sortId(array):
        return array['id']

#Обработка чата постов
@app.route('/chat', methods=['POST', 'GET'])
def chat():
    posts = requests.get(urlPosts).content
    array = (json.loads(posts))
    array.sort(key=sortId, reverse=True)
    userId = getIdFromName(session['name'])
    if request.method == "GET":
        return render_template('chat.html', data=array, userId=userId)
    elif request.method == "POST":
        index = int(request.form['index'])
        if index==5:
            nameUser = session['name']
            text = request.form['str']
            data = {'text': text, 'userID': getIdFromName(nameUser), 'name': session['name']}
            requests.post(urlPosts, data=data)
            return chatOpen()
    return render_template('chat.html', data=array, userId=userId)

#Вывод постов
@app.route('/chat/open', methods=['POST', 'GET'])
def chatOpen():
    posts = requests.get(urlPosts).content
    array = (json.loads(posts))
    array.sort(key=sortId, reverse=True)
    userId = getIdFromName(session['name'])
    return render_template('chat.html', data=array, userId=userId)

#Редактировать пост
@app.route('/editPost/<int:id>', methods=['POST', 'GET', 'DELETE','PUT'])
def edit_post(id):
    if request.method == "POST":
        nameUser = session['name']
        index = int(request.form['index'])
        idUserPost = getIdUserIdFromPost(id)
        if index == 2:
            if getIdFromName(session['name']) == idUserPost:
                text = request.form['textPut']
                if text != "":
                    data = {'userID': getIdFromName(nameUser), 'text': text, 'name': nameUser}
                    requests.put(urlPosts + str(id) + '/', data=data)
                else:
                    # Удаление поста
                    #Удалим все коментарии и лайки с этим постом
                    deleteCom(id)
                    deleteLike(id)
                    requests.delete(urlPosts + str(id))
            else:
                return chat()
        return chatOpen()
    elif request.method == "GET":
        return render_template('editPost.html')
    else:
        return "Вы делаете неверый запрос"
    return "Вы делаете неверый запрос"








# Коментарии



#Открыть коментарии
@app.route('/com/<int:id>', methods=['POST', 'GET', 'DELETE','PUT'])
def comment_request(id):
    session['postId'] = id
    if request.method == "POST":
        nameUser = session['name']
        index = int(request.form['index'])
        idUserPost = getIdUserIdFromPost(id)
        if index == 1:
            text = request.form['str']
            data = {'userID': getIdFromName(nameUser), 'postID': str(id), 'text': text, 'name': nameUser}
            requests.post(urlComment, data=data)
        elif index == 2:
            if getIdFromName(session['name']) == idUserPost:
                requests.delete(urlPosts + str(id))
        elif index == 3:
            if getIdFromName(session['name']) == idUserPost:
                text = request.form['str222']
                data = {'userID': getIdFromName(nameUser), 'postID': str(id), 'text': text, 'name':nameUser}
                requests.put(urlPosts + str(id) + '/', data=data)
        elif index == 9:
            return chat()
        comArr = json.loads(requests.get(urlComment + "?postID=" + str(id)).content)
        comArr.sort(key=sortId, reverse=True)
        userId = getIdFromName(session['name'])
        return render_template('com.html', data=comArr, userId=userId)
    elif request.method == "GET":
        comArr = json.loads(requests.get(urlComment + "?postID=" + str(id)).content)
        comArr.sort(key=sortId, reverse=True)
        userId = getIdFromName(session['name'])
        return render_template('com.html', data=comArr, userId=userId)
    else:
        return "Вы делаете неверый запрос"


#Редактировать комент
@app.route('/com/edit/<int:id>', methods=['POST', 'GET', 'DELETE','PUT'])
def edit_comm(id):
    if request.method == "POST":
        nameUser = session['name']
        index = int(request.form['index'])
        idUserCom = getIdUserIdFromComment(id)
        if index == 4:
            if getIdFromName(session['name']) == idUserCom:
                text = request.form['str']
                if request.form['str']!="":
                    data = { 'userID': getIdFromName(nameUser), 'text': text, 'name' : nameUser, 'postID': session['postId']}
                    requests.put(urlComment + str(id) + '/', data=data)
                else:
                    requests.delete(urlComment + str(id))
        return comment_request(session['postId'])
    elif request.method == "GET":
        comArr = json.loads(requests.get(urlComment + "?postID=" + str(session['postId'])).content)
        comArr.sort(key=sortId, reverse=True)
        userId = getIdFromName(session['name'])
        return render_template('editCom.html', data=comArr, userId=userId)
    else:
        return "Вы делаете неверый запрос"

#Удаление комментариев относящихся к удаленому посту
def deleteCom(id):
    comArr = json.loads(requests.get(urlComment + "?postID=" + str(id)).content)
    for el in comArr:
        if int(el['postID']) == int(id):
            requests.delete(urlComment  + str(el['id']))
    return None







# Лайки
@app.route('/like/<int:id>', methods=['POST', 'GET'])
def like_request(id):
    session['idPostLike'] = id
    Likes = requests.get(urlLike + "?postID=" + str(id)).content
    likeArr = json.loads(Likes)
    likeArr.sort(key=sortId, reverse=True)
    if request.method == "GET":
        like = False
        for el in likeArr:
            if el['userID'] == getIdFromName(session['name']):
                like = True
        return render_template('like.html', data3=likeArr, like=like)
    index = int(request.form['index'])
    if request.method == "POST":
        if index == 1:
            nameUser = session['name']
            exists = False
            for el in likeArr:
                if el["userID"] == getIdFromName(nameUser):
                    exists = True
            if exists:
                requests.delete(urlLike + str(el["id"]))
            else:
                data = {'postID': str(id), 'userID': getIdFromName(nameUser), 'name' : nameUser}
                requests.post(urlLike, data=data)

            #Считаем заново данные, так как мы их только что отредачили
            Likes = requests.get(urlLike + "?postID=" + str(id)).content
            likeArr = json.loads(Likes)
            likeArr.sort(key=sortId, reverse=True)
            like = False
            for el in likeArr:
                if el['userID'] == getIdFromName(session['name']):
                    like = True
            return render_template('like.html', data3=likeArr, like=like)
        elif index == 2:
            return chat()
    return "Вы делаете неверый запрос"


#Удаление лайков относящихся к удаленому посту
def deleteLike(id):
    Likes = requests.get(urlLike + "?postID=" + str(id)).content
    likeArr = json.loads(Likes)
    for el in likeArr:
        if int(el['postID']) == int(id):
            requests.delete(urlLike + str(el['id']))
    return None






# Вспомогательные функции
def getIdFromName(name):
    try:
        sqlite_connection = sqlite3.connect('user.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = "SELECT * from item WHERE name = " + "'" + name + "';"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
        if len(records) != 0:
            return records[0][0]
        else:
            return 0
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def getPasswordFromName(name):
    try:
        sqlite_connection = sqlite3.connect('user.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = "SELECT * from item WHERE name = " + "'" + name + "';"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
        if len(records) != 0:
            return records[0][2]
        else:
            return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def getIdUserIdFromPost(id):
    posts = requests.get(urlPosts).content
    array = json.loads(posts)
    for el in array:
        if int(el["id"]) == int(id):
            return el["userID"]

def getIdUserIdFromComment(id):
    comm = requests.get(urlComment).content
    array = json.loads(comm)
    for el in array:
        if int(el["id"]) == int(id):
            return el["userID"]

def getNameFromUserId(id):
    try:
        sqlite_connection = sqlite3.connect('user.db')
        cursor = sqlite_connection.cursor()
        id = str(id)
        sqlite_select_query = "SELECT * from item WHERE id = " + "'" + id + "';"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
        if len(records) != 0:
            return records[0][1]
        else:
            return 0

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


if __name__ == "__main__":
    app.run(debug=True)
