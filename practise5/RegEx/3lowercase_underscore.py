import re

text = input("Enter a string: ")

pattern = r"[a-z]+(_[a-z]+)+"

result = re.findall(pattern, text)

print(result)