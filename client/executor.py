"""
This classes handles the computation on the client side.

This class depends on the Connector class to handle communication with the
server.

It caches the function definition.
"""
from .connector import Connector
import pickle
import threading

class Executor():
    def __init__(self, server, port=6000, addr='http://localhost:6000'):
        self.connector = Connector(self, server, port, addr)
        self.functions = {}
        self.server = server
        threading.Thread(target=self.connector.start).start()

    def execute(self, id, func_name, data):
        """When the client received to compute any data, this id called with
        the function name and the data."""
        threading.Thread(target=self.compute, args=(id, func_name, data)).start()

    def compute(self, id, func_name, data):
        """This function does the actual computation.

        It first checks if the function definition is available. If not, it
        first loads the definition from the server.

        After computation, it returns the result to server through connector."""
        if func_name not in self.functions:
            blob = self.connector.fetch_function(func_name)
            self.functions[func_name] = pickle.loads(blob)
            print("Received function {}".format(func_name))

        func = self.functions[func_name]

        data = [func(arg) for arg in data]
        self.connector.return_data(id, data)
        print("Finished coputing for id {}".format(id))
