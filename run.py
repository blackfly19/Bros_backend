from BasicChat import app,socketio,db

if __name__ == '__main__':
    socketio.run(app,debug=True)