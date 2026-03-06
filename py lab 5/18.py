import re
text = input()
pattern = input()
print(len(re.findall(re.escape(pattern), text)))