import re
text = input()
result = re.findall(r'\d{2,}', text)
print(*result)