import re
text = input()
name, age = re.findall(r"Name:\s*(.+?),\s*Age:\s*(.+)", text)[0]
print(name, age)