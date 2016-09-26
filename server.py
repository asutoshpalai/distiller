#!/usr/bin/env python3
from flask import Flask, request
import cloudpickle, base64
import pickle
import requests
import sys, threading
from time import sleep
app = Flask(__name__)

clients = []
computes = {}
func_store = {}

id = 0
@app.route("/")
def home():
    return "Welcome to distiller"

@app.route("/test/run")
def test_compute():
    return str(compute(square, [3, 4, 5, 7, 8]))

@app.route("/test/results/<int:id>")
def test_result(id):
    if computes[id][2] == False:
        return "Results are not yet available"
    else:
        return "<br>\n".join([str(x) for x in computes[id][2]])

@app.route("/register", methods=['POST'])
def register_client():
    global clients
    ip = request.form['address']
    clients.append(ip)
    print("Received client with address {}".format(ip))
    return "success"

@app.route("/result", methods=['POST'])
def receive_results():
    id = int(request.form['id'])
    status = request.form['status']
    res = pickle.loads(base64.b64decode(request.form['data']))
    if status.lower() == 'success':
        receive(id, res)
        return "success"

@app.route("/function/<name>", methods=['GET'])
def get_function(name):
    fun = func_store[name]
    blob = cloudpickle.dumps(fun)
    return base64.b64encode(blob)

def compute(fun, params):
    global id, clients
    id = id + 1
    while(len(clients) == 0):
        sleep(1) # move this to conditions
    fun_name = fun.__name__
    func_store[fun_name] = fun
    computes[id] = [fun_name, params, False]
    print("Computing {} with data:".format(fun_name))
    print(params)
    requests.post(clients[0] + "/compute",
            data={"id": id, "func": fun_name, "data": base64.b64encode(cloudpickle.dumps(params))})
    return id

def receive(id, result):
    computes[id][2] = result
    print("received results for compute id {}".format(id))

def remote_exec(fun, params):
    print("Got remote_exec")
    id = compute(fun, params)
    while(computes[id][2] == False):
        sleep(1) # move this to conditions
    return computes[id][2]

def square(x):
    return x * x

def start_server():
    app.run()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <file_name>".format(sys.argv[0]))
        exit(1)
    file_name = sys.argv[1]
    code = ""

    threading.Thread(target=start_server).start()

    with open(file_name) as f:
        code = f.read()
    exec(code)


