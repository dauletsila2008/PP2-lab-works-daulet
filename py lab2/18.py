n = int(input().strip())
arr = [input().strip() for _ in range(n)]

first_occurrence = {}
for i, s in enumerate(arr, start=1): 
    if s not in first_occurrence:
        first_occurrence[s] = i

for s in sorted(first_occurrence.keys()):
    print(s, first_occurrence[s])