import re
stroka = input()
a = re.findall(r"\d", stroka)
print(*a)
    