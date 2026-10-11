def cubes(n):
    for i in range(1,n+1):
        yield i*i*i
a=int(input())
for numbers in cubes(a):
    print(numbers)