import re
text = input()
def double(two):
    return two.group() * 2
result = re.sub(r"\d", double, text)
print(result)