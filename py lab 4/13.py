import json
import sys

data = json.loads(sys.stdin.readline())
q = int(sys.stdin.readline())

def resolve_query(obj, query):
    i = 0
    current = obj

    while i < len(query):
        if query[i] == '.':
            i += 1
            continue

        if query[i] == '[':
            j = query.find(']', i)
            if j == -1:
                return False, None
            index_str = query[i + 1:j]
            if not index_str.isdigit():
                return False, None
            index = int(index_str)
            if not isinstance(current, list) or index < 0 or index >= len(current):
                return False, None
            current = current[index]
            i = j + 1
        else:
            j = i
            while j < len(query) and query[j] not in '.[':
                j += 1
            key = query[i:j]
            if not isinstance(current, dict) or key not in current:
                return False, None
            current = current[key]
            i = j

    return True, current

for _ in range(q):
    query = sys.stdin.readline().strip()
    ok, result = resolve_query(data, query)
    if not ok:
        print("NOT_FOUND")
    else:
        print(json.dumps(result, separators=(',', ':')))