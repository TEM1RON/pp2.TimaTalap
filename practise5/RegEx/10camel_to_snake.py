import re

text = input("Enter camel case: ")

result = re.sub(r"([A-Z])", r"_\1", text)

result = result.lower()

if result.startswith("_"):
    result = result[1:]

print(result)