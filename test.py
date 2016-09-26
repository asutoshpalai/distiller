from server.manager import Manager
import client
import threading
from time import sleep

man = Manager()
def fibo(x):
    a, b = 1, 1
    for i in range(0, x):
        a, b = b, a + b
    return a

sleep(1)
th2 = threading.Thread(target=client.start_client, args=("http://localhost:5000", 6000)).start()
th2 = threading.Thread(target=client.start_client, args=("http://localhost:5000", 7000)).start()
th2 = threading.Thread(target=client.start_client, args=("http://localhost:5000", 8000)).start()
th2 = threading.Thread(target=client.start_client, args=("http://localhost:5000", 9000)).start()
sleep(1)
result = man.remote_exec(fibo, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

assert result == [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
import os
os.kill(os.getpid(), 9)

