n = int(input())

episodes = {}

for _ in range(n):
    line = input().split()
    name = line[0]
    k = int(line[1])
    if name in episodes:
        episodes[name] += k
    else:
        episodes[name] = k

for name in sorted(episodes):
    print(name, episodes[name])
