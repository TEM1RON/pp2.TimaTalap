def squares(n):
    for i in range(n + 1):
        yield i * i


N = int(input("Enter N: "))

for value in squares(N):
    print(value)