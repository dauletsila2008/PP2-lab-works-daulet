import re
text = input()
subtext = input()
rep = input()
result = re.sub(subtext,rep,text)
print(result)