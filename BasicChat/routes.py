from BasicChat import socketio,db
from BasicChat.models import History,User,MessageSchema
from flask import request
from flask_socketio import send,emit
import json
import random
from exponent_server_sdk import DeviceNotRegisteredError,PushClient,PushMessage,PushResponseError,PushServerError
from requests.exceptions import ConnectionError,HTTPError

online_users = {}
online_usernames = []

@socketio.on('message')
def handleMessage(data):

        print('Message: ' + data[0] + ' '+data[1] + ' '+data[2])

        js = {}
        offline_user_tokens = []
        offline_users = User.query.filter(User.username.notin_(online_users)).all()

        message = History(username=online_users[request.sid],message=data[1],time=data[2])
        db.session.add(message)
        db.session.commit()

        last_message_id = History.query.order_by(History.id.desc()).first().id
        js = {"id": last_message_id,"message":data[1],"color":'black',"username":online_users[request.sid],"time":data[2]}
        send_json = json.dumps(js)
        print(send_json)
        
        if offline_users is not None:
            for user in offline_users:
                if user.username != online_users[request.sid]:
                    offline_user_tokens.append(user.uniqueId)
                    
        send(send_json,broadcast=True,include_self=False)
        send_push_message(offline_user_tokens,online_users[request.sid],data[1])

@socketio.on('connect')
def connect():
    print('Connected',request.sid)
    emit('status',1)

@socketio.on('newUser')
def newUser(values):
    print(values)
    user_exists = User.query.filter_by(uniqueId = values[0]).first()
    if user_exists is None:
        user = User(uniqueId = values[0],username = values[1])
        db.session.add(user)
        db.session.commit()
        online_users[request.sid] = user.username
        online_usernames.append(user.username)
    else:
        online_users[request.sid] = user_exists.username
        online_usernames.append(user_exists.username)

@socketio.on('user')
def existingUser(Id):
    user = User.query.filter_by(uniqueId = Id).first()
    online_users[request.sid] = user.username
    online_usernames.append(user.username)
    
@socketio.on('rowNum')
def unread_messages(last_row_id):
    print("Hi")
    m = History.query.filter(History.id > last_row_id).all()
    messages_schema = MessageSchema(many=True)
    messages = messages_schema.dump(m)
    emit('json',messages)


@socketio.on('disconnect')
def disconnect():
    if request.sid in online_users:
        online_usernames.remove(online_users[request.sid])
        del online_users[request.sid]
    print('Disconnected',request.sid)

#utility functions

#for sending notifications
def send_push_message(token,title, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        title=title,
                        sound='default',
                        body=message,
                        data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
            })
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        rollbar.report_exc_info(
            extra_data={'token': token, 'message': message, 'extra': extra})
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            })
        raise self.retry(exc=exc)

