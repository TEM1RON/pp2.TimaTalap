def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


a = int(input("Enter the starting number: "))
b = int(input("Enter the ending number: "))

for number in squares(a, b):
    print(number)