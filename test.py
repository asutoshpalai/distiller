import server
import client
import threading
from time import sleep

th1 = threading.Thread(target=server.start_server)
th1.start()

def fibo(x):
    a, b = 1, 1
    for i in range(0, x):
        a, b = b, a + b
    return a

sleep(1)
th2 = threading.Thread(target=client.start_client, args=("http://localhost:5000", 6000))
th2.start()
result = server.remote_exec(fibo, [1, 2, 3, 4])

assert result == [1, 2, 3, 5]
import os
os.kill(os.getpid(), 9)

