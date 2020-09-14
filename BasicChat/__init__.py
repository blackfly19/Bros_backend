from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
socketio = SocketIO(app,cors_allowed_origins='*')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = "47087a547430f78b85c5436470c0d88d"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)

from BasicChat import routes
