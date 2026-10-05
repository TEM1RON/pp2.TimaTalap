import re

text = input("Enter snake case: ")

words = text.split("_")

result = words[0]

for word in words[1:]:
    result = result + word.capitalize()

print(result)