# -*- coding: utf-8 -*-
from flask import Flask, render_template
from time import time
from datetime import datetime, timedelta
from flask import request
from flask import jsonify
from gevent import sleep
from gevent import monkey
from random import random

monkey.patch_all()

app = Flask(__name__)
app.debug = True

users_new_msgs = dict()


@app.route("/")
def hello():
    user_id = int(random() * 1000000000)
    users_new_msgs[user_id] = ''  # open msgs

    return render_template('index.html', user_id=user_id)


@app.route('/msg', methods=['POST'])
def get_msg():

    uid = 0

    try:
        uid = int(request.form['uid'])
        users_new_msgs[uid]  # cehck exist
    except:
        return jsonify(status='fail')

    while len(users_new_msgs[uid]) is 0:  # loop msg is empty
        sleep(0)

    now = datetime.utcnow() + timedelta(hours=9)  # GMT +0900

    ret_json = jsonify(
        status='success',
        text=users_new_msgs[uid],
        time=now.strftime('%H:%M:%S'),
        timestamp=time()
    )

    users_new_msgs[uid] = ''

    return ret_json


@app.route('/send_msg', methods=['POST'])
def recieve_msg():
    msg = request.form['msg']

    uid = 0
    try:
        uid = int(request.form['uid'])
    except:
        return jsonify(status='fail')

    if msg is not None or len(msg) is not 0 or len(msg.lstrip()) == 0:

        for (uid, old_msg) in users_new_msgs.items():
            users_new_msgs[uid] = msg
    else:
        return jsonify(status='fail')

    return jsonify(status='success')


if __name__ == "__main__":
    app.run(host="127.0.0.1", threaded=True)
