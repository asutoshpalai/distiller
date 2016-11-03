"""
This class handles the clients, distribution of a task, serialization of the
function and recombining of results.

This class internally uses Connector class to manage connection with the
clients. Due to blocking nature of the default Flask server, it spawns the
server in a separate thread.

For serialization of the functions, it uses cloudpickle and returns the pickle
blob.

For distribution of a given task, it partitions the given arguments into chunks
based on the number of clients present. Then it assigns each chuck an id with
which the client is expected to return the result.

At present, it only supports map parallelisation and not reduce parallelism.
"""

from .connector import Connector
from time import sleep
import random, math
import threading
import cloudpickle

class Manager:
    def __init__(self):
        self.functions = {} # Function storage for serialisation
        self.clients = [] # List of client's addresses
        self.computes = {} # The map of id of chunks sent to the client for computation and their results
        self.id = 0 # The last used up id
        self.connector = Connector(self)
        threading.Thread(target=self.connector.start).start()

    def register_client(self, client):
        """When a new client connects, Connector calls this function to add the
        client to internal list"""
        print("Received client {}".format(client))
        self.clients.append(client)

    def remote_exec(self, function, data):
        """This function is to be called with a function and the data (a list)
        to map using the function.
        This distributes the task among the clients and then recombines the
        result and returns the mapped values.
        """
        size = len(data)
        n = len(self.clients)

        units = math.ceil(size/n)
        lowest_id = self.id + 1
        highest_id = self.id + n
        self.id += n
        for i in range(0, n):
            chunk = data[i * units: (i + 1) * units]
            client = self.clients[i]
            id = lowest_id + i
            self.computes[id] = [function, chunk, None]
            self.compute(id, client, function, chunk)

        k = lowest_id
        while k <= highest_id:
            if self.computes[k][2] is not None:
                k += 1
            else:
                sleep(1) # move to conditions
        res = []
        for k in range(lowest_id, highest_id + 1):
            res.extend(self.computes[k][2])

        return res

    def compute(self, id, client, function, data):
        fun_name = function.__name__
        self.functions[fun_name] = function
        self.connector.client_compute(id, client, fun_name, data)

    def get_function(self, fun_name):
        """This serializes the function. When the client requests for a function
        the connector calls this function to obtain it."""
        fun = self.functions[fun_name]
        blob = cloudpickle.dumps(fun)
        return blob

    def receive_result(self, id, data):
        """When the client returns the result, connector calls this to store
        the result"""
        self.computes[id][2] = data

    def failed(self, id):
        client = random.choice(self.clients)
        fun = seld.computes[id][0]
        data = self.computes[id][1]
        self.compute(id, client, fun, data)
