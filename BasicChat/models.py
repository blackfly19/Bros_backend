from BasicChat import db,ma
from datetime import datetime as dt


class History(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    username = db.Column('username',db.String(50))
    message = db.Column('message',db.String(500))
    time = db.Column('Timestamp',db.String(20))

class User(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    uniqueId = db.Column('UniqueId',db.String(100))
    username = db.Column('username',db.String(100))

class MessageSchema(ma.Schema):
    class Meta:
        fields = ['id','username','message','time']

