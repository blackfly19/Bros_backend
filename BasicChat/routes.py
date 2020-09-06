from BasicChat import socketio,db
from BasicChat.models import History
from flask import request
from flask_socketio import send,emit
import json
import random

global_chat_users = {}
colors = {
    'Ali': 'blue',
    'Ankit':'red',
    'Sarvesh':'green',
    'Abhishek':'yellow',
    'Abhigyan': 'orange'
}

"""def generate_color():

    colors = ['green','blue','pink','black','cyan','purple','red','orange','brown','yellow']
    rnd = random.randint(0,9)
    return colors[rnd]"""


@socketio.on('message')
def handleMessage(data):

        #print('Message: ' + data[0] + ' '+data[1] + ' '+data[2])
        js = {}
        message = History(username=global_chat_users[request.sid],message=data[1],time=data[2])
        db.session.add(message)
        db.session.commit()
        last_message_id = History.query.order_by(History.id.desc()).first().id
        color = colors[global_chat_users[request.sid]]
        js = {"id": last_message_id,"message":data[1],"color":color,"username":global_chat_users[request.sid],"time":data[2]}
        send_json = json.dumps(js)
        #print(send_json)
        send(send_json,broadcast=True,include_self=False)

@socketio.on('connect')
def connect():
    print('Connected',request.sid)


@socketio.on('identifier')
def getDeviceId(values):
    #print(values)
    global_chat_users[request.sid] = values[1]
    messages = History.query.all()
    if messages is not None:
        for m in messages:
            js = {"id":m.id,"message":m.message,"color":colors[m.username],"username":m.username,"time":m.time}
            send_json = json.dumps(js)
            send(send_json,include_self=True)

@socketio.on('disconnect')
def disconnect():
    print('Disconnected',request.sid)

