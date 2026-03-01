from datetime import datetime, timedelta
import sys

def parse_moment(line):
    line = line.strip()
    date_part, tz_part = line.split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")

    sign = 1 if tz_part[3] == '+' else -1
    hours, minutes = map(int, tz_part[4:].split(':'))
    offset = timedelta(hours=hours, minutes=minutes)

    return dt - sign * offset

m1 = parse_moment(sys.stdin.readline())
m2 = parse_moment(sys.stdin.readline())

diff_seconds = abs((m1 - m2).total_seconds())
print(int(diff_seconds // 86400))