n = int(input())

def powers_of_two(limit):
    for i in range(limit + 1):
        yield 2 ** i

print(*powers_of_two(n))