import csv
import sys

filename = sys.argv[1]
cache_time = 0
with open(filename, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    prev_time = None
    time_shift = 0
    for row in reader:
        time_now = int(row[9])
        if prev_time is None:
            prev_time = time_now

        if time_now - prev_time > 1000:
            time_shift += 1000
            schedule_at = prev_time + 1000
        else:
            schedule_at = time_now - time_shift
       
        row[9] = str(schedule_at)
        print("\t".join(row))

        prev_time = time_now

