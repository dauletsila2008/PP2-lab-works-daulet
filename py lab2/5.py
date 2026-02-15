n = int(input())

if n < 1:
    print("NO")
else:
    x = 1
    while True:
        if x == n:
            print("YES")
            break
        elif x > n:
            print("NO")
            break
        x *= 2
