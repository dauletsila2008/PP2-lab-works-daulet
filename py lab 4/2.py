import sys

n = int(sys.stdin.readline())

def even_numbers(limit):
    i = 0
    while i <= limit:
        yield i
        i += 2

first = True
for num in even_numbers(n):
    if not first:
        sys.stdout.write(",")
    sys.stdout.write(str(num))
    first = False