import re
stroka = input()
podsroka = input()
b = re.findall(podsroka,stroka)
print(len(b))