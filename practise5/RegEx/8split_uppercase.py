import re

text = input("Enter a string: ")

result = re.findall(r"[A-Z][a-z]*", text)

print(result)