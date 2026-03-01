import json
import sys

obj1 = json.loads(sys.stdin.readline())
obj2 = json.loads(sys.stdin.readline())

differences = []

def to_json(value):
    return json.dumps(value, separators=(',', ':'))

def deep_diff(o1, o2, path=""):
    if isinstance(o1, dict) and isinstance(o2, dict):
        keys = sorted(set(o1.keys()) | set(o2.keys()))
        for key in keys:
            new_path = f"{path}.{key}" if path else key
            if key not in o1:
                differences.append(f"{new_path} : <missing> -> {to_json(o2[key])}")
            elif key not in o2:
                differences.append(f"{new_path} : {to_json(o1[key])} -> <missing>")
            else:
                deep_diff(o1[key], o2[key], new_path)
    else:
        if o1 != o2:
            differences.append(f"{path} : {to_json(o1)} -> {to_json(o2)}")

deep_diff(obj1, obj2)

if differences:
    for line in sorted(differences):
        print(line)
else:
    print("No differences")