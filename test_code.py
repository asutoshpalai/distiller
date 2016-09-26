def fibo(x):
    a, b = 1, 1
    for i in range(0, x):
        a, b = b, a + b
    return a

print("Starting the code....")
result = remote_exec(fibo, [4, 2000, 300, 100])
print("Finished computation, result:")
print(result)
