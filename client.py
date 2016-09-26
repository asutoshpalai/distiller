#!/usr/bin/env python3
from flask import Flask, request
import requests
import sys
import cloudpickle, pickle, base64
import threading

function_store = {}

app = Flask(__name__)
server = False

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

def start_client(ser, port):
    global server
    server = ser
    requests.post("{}/register".format(server), data = {"address": "http://localhost:{}".format(port)})
    app.run(port=port)

def stop_client():
    app.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("""
                Usage:
                {} <server_root> [<port>=6000]
                """.format(sys.argv[0]))
        exit(1)

    server = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) == 3 else 6000

    start_client(server, port)

