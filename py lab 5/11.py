import re
text = input()
result = re.findall(r"[A-Z]", text)
print(len(result))