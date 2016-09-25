#!/usr/bin/env python3
from flask import Flask, request
import requests
import sys
import cloudpickle, pickle, base64
import threading

function_store = {}

if len(sys.argv) != 2:
    print("""
            Usage:
            {} <server_root>
            """.format(sys.argv[0]))
    exit(1)

server = sys.argv[1]

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to distiller client"

@app.route("/compute", methods=['POST'])
def receive_compute():
    id = request.form['id']
    func_name = request.form['func']
    data = pickle.loads(base64.b64decode(request.form['data']))

    threading.Thread(target=compute, args=(id, func_name, data, )).start()
    print("Received request to compute func {} with {} args".format(func_name, len(data)))
    return "computing..."

def compute(id, func_name, data):
    if func_name not in function_store:
        r = requests.get("{}/function/{}".format(server, func_name))
        function_store[func_name] = pickle.loads(base64.b64decode(r.text))
        print("Received function {}".format(func_name))

    func = function_store[func_name]

    data = [func(arg) for arg in data]
    ret = base64.b64encode(cloudpickle.dumps(data))

    print(data)
    r = requests.post("{}/result".format(server),
            data={"id": id, "status": "success", "data": ret})
    print("Finished coputing for id {}".format(id))

if __name__ == "__main__":
    requests.post("{}/register".format(server), data = {"address": "http://localhost:6000"})
    app.run(port=6000)
