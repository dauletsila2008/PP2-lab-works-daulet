s = input()


if "+" in s:
    op = "+"
elif "-" in s:
    op = "-"
else:
    op = "*"


left = s.split(op)[0]
right = s.split(op)[1]

def to_number(part):
    n = 0
    i = 0
    while i < len(part):
        t = part[i:i+3]
        if t == "ZER": d = 0
        elif t == "ONE": d = 1
        elif t == "TWO": d = 2
        elif t == "THR": d = 3
        elif t == "FOU": d = 4
        elif t == "FIV": d = 5
        elif t == "SIX": d = 6
        elif t == "SEV": d = 7
        elif t == "EIG": d = 8
        elif t == "NIN": d = 9
        n = n * 10 + d
        i += 3
    return n

n1 = to_number(left)
n2 = to_number(right)

if op == "+": res = n1 + n2
elif op == "-": res = n1 - n2
else: res = n1 * n2

res_s = ""
for d in str(res):
    if d == "0": res_s += "ZER"
    elif d == "1": res_s += "ONE"
    elif d == "2": res_s += "TWO"
    elif d == "3": res_s += "THR"
    elif d == "4": res_s += "FOU"
    elif d == "5": res_s += "FIV"
    elif d == "6": res_s += "SIX"
    elif d == "7": res_s += "SEV"
    elif d == "8": res_s += "EIG"
    elif d == "9": res_s += "NIN"

print(res_s)