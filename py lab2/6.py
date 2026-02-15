n = int(input())
sequence = list(map(int, input().split()))
maximum = sequence[0]
for i in range(1, n):
    if sequence[i] > maximum:
        maximum = sequence[i]
print(maximum)
    


