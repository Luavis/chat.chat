# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from time import time
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

initial_msg = [
    '##    ##    ######     ##           ##           ####',
    '##    ##    ##            ##           ##         ##    ##',
    '######   ######     ##           ##         ##    ##',
    '##    ##   ##            ##           ##         ##    ##',
    '##    ##   ######    ######  ######    ####',
    '',
    'Welcome to 채트채트, ',
    'This server is purpose on http2/long polling/web socket benchtest',
    'Develop by Luavis',
]


@app.route("/")
def hello():
    return render_template('index.html')


@socketio.on('test_msg', namespace="/msg")
def test_msg(data):

    now = datetime.utcnow() + timedelta(hours=9)  # GMT +0900

    for msg in initial_msg:
        emit('recv_msg', {
            'text': msg,
            'time': now.strftime('%H:%M:%S'),
            'timestamp': time(),
        })

@socketio.on('send_msg', namespace="/msg")
def recieve_msg(data):

    msg = data.get('msg')

    if msg is not None:

        now = datetime.utcnow() + timedelta(hours=9)  # GMT +0900

        emit("recv_msg", {
            'text': msg,
            'time': now.strftime('%H:%M:%S'),
            'timestamp': time(),
        }, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
