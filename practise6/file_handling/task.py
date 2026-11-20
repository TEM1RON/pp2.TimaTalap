import os
with open("values.txt","w") as file:
    file.write("10 \n")
    file.write("3.5 \n")
    file.write("7 \n")
    file.write("hello \n")

with open("values.txt", "r") as file:
    lines = file.readlines()
    print (lines)

with open("values.txt", "a") as file:
    file.write("42 \n")
    
with open("values.txt", "r") as file:
    lines = file.readlines()
    print (lines)

with open("values.txt", "r") as file:
    for num in len(lines):
        if type(num):
            print("its a num")
        else:
            print("hello")
        

os.remove("values.txt")