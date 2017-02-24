# -*- encoding: utf-8 -*-

import flask
import gevent.pywsgi
import gevent.monkey
import os

import servicehub

gevent.monkey.patch_all()

app = flask.Flask(__name__)
ctx = servicehub.Context("172.16.8.1:6619")

@app.route("/on_message", methods = ["POST"])
def on_message():
    d = flask.request.get_json(force = True)

    return flask.jsonify({
        "err": 0,
        "msg": "OK",
        "content": "Hello " + d["chat_id"] + ": " + d["content"]
    })

ctx.register("HydroCloud_ChatService_testing", "http://172.16.10.1:7325", True)

try:
    gevent.pywsgi.WSGIServer(("0.0.0.0", 7325), app).serve_forever()
except KeyboardInterrupt:
    os._exit(0)
