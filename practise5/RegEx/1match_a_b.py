import re

text = input("Enter a string: ")

pattern = r"ab*"

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")