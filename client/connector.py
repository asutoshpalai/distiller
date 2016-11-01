from flask import Flask, request
import requests
import base64
import cloudpickle, pickle

class Connector():
    def __init__(self, executor, server, port, addr):
        self.app = Flask(__name__)
        self.executor = executor
        self.port = port # TODO parse client address to get port
        self.server = server
        self.addr = addr
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/compute", "compute", self.compute, methods=['POST'])

    def start(self):
        print("Starting client...")
        requests.post("{}/register".format(self.server), data = {"address": "{}".format(self.addr)})
        self.app.run(port=self.port)

    def fetch_function(self, name):
        r = requests.get("{}/function/{}".format(self.server, name))
        return base64.b64decode(r.text)

    def return_data(self, id, data):
        ret = base64.b64encode(cloudpickle.dumps(data))
        r = requests.post("{}/result".format(self.server),
                data={"id": id, "status": "success", "result": ret})


    def index(self):
        return "Welcome to distill client"

    def compute(self):
        id = request.form['id']
        func_name = request.form['function']
        data = pickle.loads(base64.b64decode(request.form['data']))

        self.executor.execute(id, func_name, data)
        self.app.logger.info("Received request to compute func {} with {} args".format(func_name, len(data)))
        return "computing..."



