n = int(input())
s = input().split()

max_value = int(s[0])
position = 1

for i in range(1, n):
    if int(s[i]) > max_value:
        max_value = int(s[i])
        position = i + 1

print(position)

