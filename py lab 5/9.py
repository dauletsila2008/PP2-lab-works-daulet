import re
text = input()
result = re.findall(r"\b\w{3}\b", text)
print(len(result))