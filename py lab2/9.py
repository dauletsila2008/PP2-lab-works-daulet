n = int(input())
a = input().split()

mn = int(a[0])
mx = int(a[0])

for i in range(1, n):
    x = int(a[i])
    if x < mn:
        mn = x
    if x > mx:
        mx = x

for i in range(n):
    if int(a[i]) == mx:
        a[i] = str(mn)
print(' '.join(a))
