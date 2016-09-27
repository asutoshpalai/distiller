def fibo1(x):
    a, b = 1, 1
    for i in range(0, x):
        a, b = b, a + b
    return a

result = remote_exec(fibo1, [4, 2, 3, 1])
assert result == [5, 2, 3, 1]
