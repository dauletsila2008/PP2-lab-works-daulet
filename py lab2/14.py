n = int(input())
a = list(map(int, input().split()))

freq = {}

for x in a:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

max_freq = 0
answer = None

for x in freq:
    if freq[x] > max_freq or (freq[x] == max_freq and x < answer):
        max_freq = freq[x]
        answer = x

print(answer)
