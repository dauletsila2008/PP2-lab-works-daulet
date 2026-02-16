n = int(input())
a = list(map(int, input().split()))

max_value = a[0]
position = 1

for i in range(1, n):
    if a[i] > max_value:
        max_value = a[i]
        position = i + 1

print(position)


