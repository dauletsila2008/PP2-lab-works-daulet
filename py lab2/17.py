n = int(input())

freq = {}

for _ in range(n):
    number = input()
    if number in freq:
        freq[number] += 1
    else:
        freq[number] = 1

count = 0
for number in freq:
    if freq[number] == 3:
        count += 1

print(count)
