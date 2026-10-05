import re

text = input("Enter a string: ")

pattern = r"a.*b"

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")