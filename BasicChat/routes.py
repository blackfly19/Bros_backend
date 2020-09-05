from BasicChat import socketio,db
from BasicChat.models import History,User
from flask import request
from flask_socketio import send,emit
import json
import numpy as np

global_chat_users = {}

def generate_random_name():

    colors = ['Green','Blue','Pink','Black','Cyan','Purple','Red','Orange','Brown']
    #colors = ['#ff2400','#ff2400','#ff2400','#ff2400','#ff2400','#ff2400','#ff2400','#ff2400','#ff2400','#ff2400']
    adjectives = ['Cool','Awesome','Dangerous','Cunning','Adventurous','Fearless','Brave','Charming','Intelligent','Amazing']
    animal = ['Tiger','Penguin','Eagle','Bear','Panda','Wolf','Seal','Shark','Koala','Rabbit']

    name_rand = np.random.randint(10,size=3)
    return adjectives[name_rand[1]] +colors[name_rand[0]] +animal[name_rand[2]],colors[name_rand[0]]


@socketio.on('message')
def handleMessage(data):

        print('Message: ' + data[0] + ' '+data[1] + ' '+data[2])
        js = {}
        message = History(message=data[1])
        db.session.add(message)
        db.session.commit()
        last_message_id = History.query.order_by(History.id.desc()).first().id
        sender = global_chat_users[request.sid]
        js = {"id": last_message_id,"message":data[1],"color":sender[1].lower(),"username":sender[0],"time":data[2]}
        send_json = json.dumps(js)
        print(send_json)
        send(send_json,broadcast=True,include_self=False)

@socketio.on('connect')
def connect():
    name = generate_random_name()
    print('Connected',name[0])
    global_chat_users[request.sid] = name

@socketio.on('identifier')
def getDeviceId(values):
    print(values)
    user = User(deviceId=values[0],name=values[1],username=global_chat_users[request.sid][0])
    db.session.add(user)
    db.session.commit()

@socketio.on('disconnect')
def disconnect():
    disconnected_device = global_chat_users[request.sid]
    print('Disconnected',disconnected_device)

