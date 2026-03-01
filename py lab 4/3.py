import sys

n = int(sys.stdin.readline())

def gen(limit):
    for i in range(0, limit + 1, 12):
        yield i

first = True
for x in gen(n):
    if not first:
        sys.stdout.write(" ")
    sys.stdout.write(str(x))
    first = False