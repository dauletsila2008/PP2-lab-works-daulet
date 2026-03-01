import sys
import math

r = float(sys.stdin.readline())
x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

dx = x2 - x1
dy = y2 - y1

a = dx * dx + dy * dy
b = 2 * (x1 * dx + y1 * dy)
c = x1 * x1 + y1 * y1 - r * r


discriminant = b * b - 4 * a * c

if discriminant < 0:
    
    inside = (x1 * x1 + y1 * y1 <= r * r) and (x2 * x2 + y2 * y2 <= r * r)
    if inside:
        length = math.hypot(dx, dy)
    else:
        length = 0.0
else:
    sqrt_d = math.sqrt(discriminant)
    t1 = (-b - sqrt_d) / (2 * a)
    t2 = (-b + sqrt_d) / (2 * a)

    t_low = max(0.0, min(t1, t2))
    t_high = min(1.0, max(t1, t2))

    if t_low > t_high:
        inside = (x1 * x1 + y1 * y1 <= r * r) and (x2 * x2 + y2 * y2 <= r * r)
        if inside:
            length = math.hypot(dx, dy)
        else:
            length = 0.0
    else:
        length = (t_high - t_low) * math.hypot(dx, dy)

print(f"{length:.10f}")