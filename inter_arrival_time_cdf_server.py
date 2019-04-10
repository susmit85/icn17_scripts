import sys 
import csv
import operator
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import re

    

log = sys.argv[1]
name_dict = {}

with open(log, 'r') as f:
    reader = f.read()
    for row in reader.split('\n'):
        ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', row )
        try:
            ip_addr = ip[0]
        except IndexError:
            print("Error on line ", row)
            continue
 
        split_row = row.split('\t')
        name = split_row[3]
        time = int(split_row[8])
        if time < 1317153616 or time > 1458075474:
            continue
       
#        {ip:{name1:[t1, t2]}, {name2:[t1,t2]}]
        try:
            name_dict[name].append(time)
        except KeyError:
            name_dict[name] = [time]

                   
#print(client_dict)            
total_average_dist = []
total_median_dist = []
for key, val in name_dict.items():
    server_avg = []
    server_median = []
    sorted_f_list = sorted(val)
    if len(sorted_f_list) > 1:
        intervals = [sorted_f_list[i] - sorted_f_list[i-1] for i in range(1, len(sorted_f_list))]
        average = np.mean(intervals)
        median = np.median(intervals)
        total_average_dist.append(average)
        total_median_dist.append(median)
#print(total_average_dist, total_median_dist)

total_average_dist.sort()
total_median_dist.sort()

bins = [x*5 for x in range(100)]
print(bins)


hist_avg, bin_edges_avg= np.histogram(total_average_dist, bins)
hist_median, bin_edges_median= np.histogram(total_median_dist, bins)

y_avg = [i/sum(hist_avg) for i in hist_avg]
y_med = [i/sum(hist_median) for i in hist_median]

y_avg_cumsum = [0]
y_avg_cumsum.extend(np.cumsum(y_avg))
y_med_cumsum = [0]
y_med_cumsum.extend(np.cumsum(y_med))
print(y_avg_cumsum, y_med_cumsum)

fig = plt.figure()
ax1 = fig.add_subplot(111)

print(len(bin_edges_median), len(y_avg_cumsum))
ax1.plot(bins, y_avg_cumsum, label="CDF of Average Inter-request time at server", linestyle="-")
ax1.plot(bins, y_med_cumsum, label="CDF of Median Inter-request time at server", linestyle="--")
ax1.set_xlabel("Time(s)")
ax1.set_ylabel("Distribution of request Intervals")

#labels = [str(x) for x in range(bins[-1]) if x%100==0]

ax1.grid()
ax1.legend(loc="lower right")

#plt.xticks(bins, labels, rotation='90')
plt.savefig('inter_arrival_cdf_server_started.pdf', dpi=300, bbox_inches='tight')


