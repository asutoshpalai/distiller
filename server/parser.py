"""
This class handles parsing and execution of files.
It evaluates the file in an environment with a special function `remote_exec`.

`remote_exec` function is used by the programs to pass the function and the data
that is to be executed on the client side and result is to be returned.
"""

from .manager import Manager

class Parser():
    def __init__(self, manager = None):
        if manager == None:
            manager = Manager()
        self.manager = manager

    def exec_file(self, file_path):
        """This function can be called with a file to run it."""
        with open(file_path) as f:
            code = f.read()

        exec(code, {'remote_exec': self.manager.remote_exec}, {})
