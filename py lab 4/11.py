import json
import sys

source = json.loads(sys.stdin.readline())
patch = json.loads(sys.stdin.readline())

def apply_patch(src, pch):
    for key, value in pch.items():
        if value is None:
            src.pop(key, None)
        elif key in src and isinstance(src[key], dict) and isinstance(value, dict):
            apply_patch(src[key], value)
        else:
            src[key] = value
    return src

result = apply_patch(source, patch)

print(json.dumps(result, separators=(',', ':'), sort_keys=True))