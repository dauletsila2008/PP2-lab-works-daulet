import re
text = input()
email = re.search(r"\S+@\S+\.\S+", text)
if email:
    print(email.group())
else:
    print("No email")
