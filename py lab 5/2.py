import re
stroka = input()
podstrok = input()
if re.search(podstrok,stroka):
    print("Yes")
else:
    print("No")