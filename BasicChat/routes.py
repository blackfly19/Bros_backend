from BasicChat import socketio,db
from BasicChat.models import History,User,MessageSchema
from flask import request
from flask_socketio import send,emit
import json
import random

global_chat_users = {}

@socketio.on('message')
def handleMessage(data):

        print('Message: ' + data[0] + ' '+data[1] + ' '+data[2])
        js = {}
        message = History(username=global_chat_users[request.sid],message=data[1],time=data[2])
        db.session.add(message)
        db.session.commit()
        last_message_id = History.query.order_by(History.id.desc()).first().id
        js = {"id": last_message_id,"message":data[1],"color":'black',"username":global_chat_users[request.sid],"time":data[2]}
        send_json = json.dumps(js)
        print(send_json)
        send(send_json,broadcast=True,include_self=False)

@socketio.on('connect')
def connect():
    print('Connected',request.sid)


@socketio.on('newUser')
def newUser(values):
    print(values)
    user = User(uniqueId = values[0],username = values[1])
    db.session.add(user)
    db.session.commit()
    global_chat_users[request.sid] = values[1]

@socketio.on('user')
def existingUser(Id):
    user = User.query.filter_by(uniqueId = Id).first()
    global_chat_users[request.sid] = user.username
    
@socketio.on('rowNum')
def unread_messages(last_row_id):
    print("Hi")
    m = History.query.filter(History.id > last_row_id).all()
    messages_schema = MessageSchema(many=True)
    messages = messages_schema.dump(m)
    emit('json',messages)
    """runs = last_row_id
    num_messages = len(m)
    while runs < num_messages:
        js = {"id":m[runs].id,"message":m[runs].message,"color":'black',"username":m[runs].username,"time":m[runs].time}
        send_json = json.dumps(js)
        send(send_json,include_self=True)
        runs = runs + 1"""

@socketio.on('disconnect')
def disconnect():
    del global_chat_users[request.sid]
    print('Disconnected',request.sid)

