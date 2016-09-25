#!/usr/bin/env python3
from flask import Flask, request
import cloudpickle, base64
import pickle
import requests
app = Flask(__name__)

clients = []

computes = {}
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

@app.route("/function/<name>", methods=['GET'])
def get_function(name):
    fun = globals()[name]
    blob = cloudpickle.dumps(fun)
    return base64.b64encode(blob)

def compute(fun, params):
    global id
    id = id + 1
    fun_name = fun.__name__
    computes[id] = [fun_name, params, False]
    print("Computing {} with data:".format(fun_name))
    print(params)
    requests.post(clients[0] + "/compute",
            data={"id": id, "func": fun_name, "data": base64.b64encode(cloudpickle.dumps(params))})
    return id

def receive(id, result):
    computes[id][2] = result
    print("received results for compute id {}".format(id))

def square(x):
    return x * x

if __name__ == "__main__":
    app.run()
