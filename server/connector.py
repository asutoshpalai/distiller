from flask import Flask, request
import requests
import base64
import cloudpickle, pickle

class Connector():
    def __init__(self, manager, port = 5000):
        self.app = Flask(__name__)
        self.manager = manager
        self.port = port

        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/register", "register_client", self.register_client, methods=['POST'])
        self.app.add_url_rule("/function/<name>", "fetch_function", self.fetch_function)
        self.app.add_url_rule("/result", "result", self.result, methods=['POST'])

    def start(self):
        print("Starting server...")
        self.app.run(port=self.port)

    def client_compute(self, id, client, function, data):
        b64 = base64.b64encode(cloudpickle.dumps(data))
        requests.post("{}/compute".format(client),
                data={"id": id, "function":function, "data": b64})

    def index(self):
        return "Welcome to distill server"

    def register_client(self):
        addr = request.form['address']
        self.manager.register_client(addr)
        return "success"

    def fetch_function(self, name):
        blob = self.manager.get_function(name)
        return base64.b64encode(blob)

    def result(self):
        id = int(request.form['id'])
        status = request.form['status']
        if status.lower() == 'success':
            res = pickle.loads(base64.b64decode(request.form['result']))
            self.manager.receive_result(id, res)
            return "Success"
        else:
            self.manager.failed(id)
            return "Failure"
