from BasicChat import db
from datetime import datetime as dt


class History(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    message = db.Column('message',db.String(500))
    time = db.Column('Timestamp',db.DateTime,default = dt.now())

class User(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    deviceId = db.Column('deviceId',db.String(100))
    name = db.Column('name',db.String(150))
    username = db.Column('username',db.String(64))
