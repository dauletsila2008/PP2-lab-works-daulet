import math

nums = list(map(int, input().split()))
primes = []

for n in nums:
    if n > 1:
        for i in range(2, int(math.isqrt(n)) + 1):
            if n % i == 0:
                break
        else:
            primes.append(n)

if primes:
    print(*primes)
else:
    print("No primes")