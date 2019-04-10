import csv
import numpy as np
import sys

log_file = sys.argv[1]

user_dict = {}
with open(log_file, 'r') as l:
    reader = csv.reader(l, delimiter='\t')
    for row in reader:
        user = row[1]
        time = int(row[8])
        try:
            user_dict[user].append(time)
        except KeyError:
            user_dict[user] = [time]

for key, value in user_dict.items():
    value_list = sorted(value)
    diff_list = [t -s for s, t in zip(value_list, value_list[1:])]
    print(len(value_list), np.median(diff_list), np.average(diff_list))

