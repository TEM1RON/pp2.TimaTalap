def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


n = int(input("Enter a number: "))

result = []

for number in even_numbers(n):
    result.append(str(number))

print(",".join(result))