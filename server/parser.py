from manager import Manager

manager = Manager()

file_path = input("Enter the file path: ")
with open(file_path) as f:
    code = f.read()

exec(code, {}, {})
