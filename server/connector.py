"""
This class manages the connections to and from the clients.

This internals of this class is totally independent of other class, so that
if required the protocol can be changed easily without requiring any change in
other classes.

This uses HTTP protocol to intreract with the client.
"""

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
        """Starts the internal server to be able to receive connections from
        the clients."""
        print("Starting server...")
        self.app.run(port=self.port)

    def client_compute(self, id, client, function, data):
        """Sends the relevent data to the client (specified by the address
        passed in `client`) to perform the computations."""
        b64 = base64.b64encode(cloudpickle.dumps(data))
        requests.post("{}/compute".format(client),
                data={"id": id, "function":function, "data": b64})

    def index(self):
        return "Welcome to distill server"

    def register_client(self):
        """Server request handler to receive requests at /register.
        It expects the client to pass it's own address."""
        addr = request.form['address']
        self.manager.register_client(addr)
        return "success"

    def fetch_function(self, name):
        """Server request handler to receive requests at /function/<name>.
        It returns the picked version of the function by name <name> in
        Base64 encoded string.
        """
        blob = self.manager.get_function(name)
        return base64.b64encode(blob)

    def result(self):
        """Server request handler to receive requests at /result.
        It accepts the result of computation from the clients and passes the
        same to manager object.
        """
        id = int(request.form['id'])
        status = request.form['status']
        if status.lower() == 'success':
            res = pickle.loads(base64.b64decode(request.form['result']))
            self.manager.receive_result(id, res)
            return "Success"
        else:
            self.manager.failed(id)
            return "Failure"
