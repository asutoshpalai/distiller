from .manager import Manager

class Parser():
    def __init__(self, manager = None):
        if manager == None:
            manager = Manager()
        self.manager = manager

    def exec_file(self, file_path):
        with open(file_path) as f:
            code = f.read()

        exec(code, {'remote_exec': self.manager.remote_exec}, {})
