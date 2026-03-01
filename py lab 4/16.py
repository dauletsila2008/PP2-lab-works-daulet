from datetime import datetime, timedelta
import sys

def parse_datetime(line):
    line = line.strip()
    date_part, time_part, tz_part = line.split()
    dt = datetime.strptime(date_part + " " + time_part, "%Y-%m-%d %H:%M:%S")

    sign = 1 if tz_part[3] == '+' else -1
    hours, minutes = map(int, tz_part[4:].split(':'))
    offset = timedelta(hours=hours, minutes=minutes)

    return dt - sign * offset

start_utc = parse_datetime(sys.stdin.readline())
end_utc = parse_datetime(sys.stdin.readline())

duration = int((end_utc - start_utc).total_seconds())
print(duration)