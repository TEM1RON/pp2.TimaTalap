import re

text = input("Enter a string: ")

pattern = r"[A-Z][a-z]+"

result = re.findall(pattern, text)

print(result)