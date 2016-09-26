from .connector import Connector
from time import sleep
import random, math
import threading
import cloudpickle

class Manager:
    def __init__(self):
        self.functions = {}
        self.clients = []
        self.computes = {}
        self.id = 0
        self.connector = Connector(self)
        threading.Thread(target=self.connector.start).start()

    def register_client(self, client):
        print("Received client {}".format(client))
        self.clients.append(client)

    def remote_exec(self, function, data):
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
            print(self.computes[k][2])
            res.extend(self.computes[k][2])

        return res

    def compute(self, id, client, function, data):
        fun_name = function.__name__
        self.functions[fun_name] = function
        self.connector.client_compute(id, client, fun_name, data)

    def get_function(self, fun_name):
        fun = self.functions[fun_name]
        blob = cloudpickle.dumps(fun)
        return blob

    def receive_result(self, id, data):
        self.computes[id][2] = data

    def failed(self, id):
        client = random.choice(self.clients)
        fun = seld.computes[id][0]
        data = self.computes[id][1]
        self.compute(id, client, fun, data)
