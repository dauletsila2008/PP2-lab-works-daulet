def is_valid(a):
    b = list(map(int, str(a)))
    c = 0

    for i in range(len(b)):
        if b[i] % 2 != 0:
            c += 1

    if c == 0:
        print("Valid")
    else:
        print("Not valid")

a = int(input())
is_valid(a)