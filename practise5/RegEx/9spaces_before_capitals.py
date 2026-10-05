import re

text = input("Enter a string: ")

result = re.sub(r"([A-Z])", r" \1", text)

print(result.strip())