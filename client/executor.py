from .connector import Connector
import pickle
import threading

class Executor():
    def __init__(self, server, port=6000):
        self.connector = Connector(self, server, port)
        self.functions = {}
        self.server = server
        threading.Thread(target=self.connector.start).start()

    def execute(self, id, func_name, data):
        threading.Thread(target=self.compute, args=(id, func_name, data)).start()


    def compute(self, id, func_name, data):
        if func_name not in self.functions:
            blob = self.connector.fetch_function(func_name)
            self.functions[func_name] = pickle.loads(blob)
            print("Received function {}".format(func_name))

        func = self.functions[func_name]

        data = [func(arg) for arg in data]
        self.connector.return_data(id, data)
        print("Finished coputing for id {}".format(id))
