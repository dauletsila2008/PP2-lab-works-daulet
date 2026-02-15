n = int(input())
s = input().split()

count = 0
for i in range(n):
    if int(s[i]) > 0:
        count += 1

print(count)
