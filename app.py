from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from time import time
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)


@app.route("/")
def hello():
    return render_template('index.html')


@socketio.on('send_msg', namespace="/msg")
def recieve_msg(data):

    msg = data.get('msg')

    if msg is not None:

        now = datetime.utcnow() + timedelta(hours=9)  # GMT +0900

        emit("recv_msg", {
            'text': msg,
            'time': now.strftime('%H:%M:%S'),
            'timestamp': time(),
        })


if __name__ == "__main__":
    socketio.run(app)
