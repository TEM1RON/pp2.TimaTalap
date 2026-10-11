import re

def words(a):
    pattern=r"g.*ing"
    print(re.findall(pattern, a))
    
    
a = input()
print(words(a))