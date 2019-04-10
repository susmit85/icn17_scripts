import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
import datetime
from operator import truediv
import csv
import time

success =0
failure = 0

ip_dict = {}
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        time,ip,flag,req_size,xfer_size = int(line[8]), line[5], line[10], int(line[14]), int(line[15])
#        print(time,ip, flag,req_size,xfer_size)
        try:
           ip_dict[ip][0] += 1 if xfer_size == req_size and req_size > 0 else 0
           ip_dict[ip][1] += 1 if req_size < 0 or xfer_size < 0 or req_size > xfer_size else 0
        except:
            ip_dict[ip] = [0,1] if req_size < 0 or req_size > xfer_size else [1,0]

percentage_failure = {}
a_10_bucket = []
a_90_bucket = []
a_100_bucket = []
for key, val in ip_dict.items():
    print(key, val)
    percentage_failure[key] = (int(val[1])*100)/(int(val[0])+int(val[1])) if int(val[0])+int(val[1]) > 0 else 0
    if percentage_failure[key] <= 10:
        a_10_bucket.append(key)
    elif 11 <= percentage_failure[key] <= 90:
        a_90_bucket.append(key)
    else:
        a_100_bucket.append(key)

print(a_10_bucket, a_90_bucket, a_100_bucket)        

a_10_bucket_dups = set()
a_90_bucket_dups = set()
a_100_bucket_dups = set()

a_dup_10_timeline = []
a_dup_90_timeline = []
a_dup_100_timeline = []

with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        time,file_name,ip = int(line[8]), line[3], line[5]
        if ip in a_10_bucket:
            if file_name in a_10_bucket_dups:
                a_dup_10_timeline.append(time)
            else:
                a_10_bucket_dups.add(file_name)
        elif ip in a_90_bucket:
            if file_name in a_90_bucket_dups:
                a_dup_90_timeline.append(time)
            else:
                a_90_bucket_dups.add(file_name)
        elif ip in a_100_bucket:
            if file_name in a_100_bucket_dups:
                a_dup_100_timeline.append(time)
            else:
                a_100_bucket_dups.add(file_name)
        
print(a_dup_10_timeline, a_dup_90_timeline, a_dup_100_timeline)


bins = [x for x in range(1379894400,1469923200, 3600*24)]

secs = mdates.epoch2num(bins)
a_10_hist, bin_edges = np.histogram(a_dup_10_timeline, bins=bins)
a_90_hist, bin_edges = np.histogram(a_dup_90_timeline, bins=bins)
a_100_hist, bin_edges = np.histogram(a_dup_100_timeline, bins=bins)

fig = plt.figure()
ax1 = fig.add_subplot(311)

ax1.set_yscale('log')
ax1.plot(secs[1:], a_10_hist, color='blue', label="Less than 10% transfers are partial")

ax2= fig.add_subplot(312, sharex=ax1, sharey=ax1)
ax2.set_yscale('log')
ax2.plot(secs[1:], a_90_hist, color='blue', label="10-90% transfers are partial")

ax3 = fig.add_subplot(313, sharex=ax1, sharey=ax1)
ax3.set_yscale('log')
ax3.plot(secs[1:], a_100_hist, color='blue', label="More than 90% transfers are partial")


ax1.legend(loc="upper left")
ax2.legend(loc="upper left")
ax3.legend(loc="upper left")
ax2.set_ylabel("Number of Duplicate Requests", fontsize=16)

ax1.tick_params(axis='both', which='major', labelsize=16)
ax2.tick_params(axis='both', which='major', labelsize=16)
ax3.tick_params(axis='both', which='major', labelsize=16)


ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),
          ncol=3, fancybox=True, shadow=True)

ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),
          ncol=3, fancybox=True, shadow=True)

ax3.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),
          ncol=3, fancybox=True, shadow=True)


plt.subplots_adjust(hspace=0.5)
# Choose your xtick format string
date_fmt = '%Y-%m-%d'

# Use a DateFormatter to set the data to the correct format.
date_formatter = mdates.DateFormatter(date_fmt)
ax1.xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()

plt.savefig('failure_10.pdf', dpi=400, bbox_inches='tight')
