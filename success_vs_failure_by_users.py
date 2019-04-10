import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
import datetime
from operator import truediv
import csv


success = []
failure = []
user_failure = {}
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
#       print(line)
        time,user,flag,req_size,xfer_size = int(line[8]), line[1], line[10], int(line[14]), int(line[15])
#        print(time,flag,req_size,xfer_size)
        if flag == 'f' or req_size > xfer_size or req_size < 0:
            try:
                user_failure[user][0] += 1
            except:
                user_failure[user] = [0,1]
            
        else:
            try:
                user_failure[user][1] += 1
            except:
                user_failure[user] = [1,0]


failure_percent_list = []
x_axis = []
index = -1
for item in user_failure.values():
    index += 1
    x_axis.append(index)
    print(item)
    success = item[1]
    failure = item[0]
    failure_percent = (failure*100.0)/(success+failure) if success+failure > 0 else 100
    print(failure_percent)
    failure_percent_list.append(failure_percent)

print(x_axis, sorted(failure_percent_list))
fig = plt.figure()


ax1 = fig.add_subplot(111)


ax1.bar(x_axis, sorted(failure_percent_list), 0.1, color="blue", label="Percentage of failed requests")

ax1.set_ylabel("Percentage of failed requests")
ax1.set_xlabel("Users (each line = 1 user)")

fig.savefig("failed_requests_by_user.png", dpi=300)
