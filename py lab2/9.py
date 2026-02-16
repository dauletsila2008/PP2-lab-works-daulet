n = int(input())
a = list(map(int, input().split()))

mn = a[0]
mx = a[0]

for i in range(1, n):
    if a[i] < mn:
        mn = a[i]
    if a[i] > mx:
        mx = a[i]

for i in range(n):
    if a[i] == mx:
        a[i] = mn

print(*a)

