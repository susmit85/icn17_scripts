import sys 
import csv
import operator
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import re


def calculate_daily_average(time_list):
    sorted_time_list = sorted(time_list)
    print(sorted_time_list)
    intervals = [sorted_time_list[i]-sorted_time_list[i-1] for i in range(1,len(sorted_time_list))]
    filtered_intervals = [sorted_time_list[i]-sorted_time_list[i-1] for i in range(1,len(sorted_time_list)) if
    sorted_time_list[i] - sorted_time_list[i-1] < 100]

    avg = np.mean(intervals)
    median = np.median(intervals)

    f_avg = np.mean(filtered_intervals)
    f_median = np.median(filtered_intervals)
    print(intervals, filtered_intervals, avg, median, f_avg, f_median)

    
    

log = sys.argv[1]
client_dict = {}

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
            if name in client_dict[ip_addr]:
                client_dict[ip_addr][name].append(time)
            else:
                client_dict[ip_addr][name] = [time]
        except KeyError:
            client_dict[ip_addr] = {name:[time]}

                   
total_average_dist = []
total_median_dist = []

#print(client_dict)            
for key, val in client_dict.items():
 #   print(key, val)
#key = IP

    ip_avg = []
    ip_median = []
    for f_name, f_size_l in val.items():

        sorted_f_size_l = sorted(f_size_l)
        if len(f_size_l) > 1:
            intervals = [sorted_f_size_l[i] - sorted_f_size_l[i-1] for i in range(1, len(sorted_f_size_l))]
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
ax1.plot(bins, y_avg_cumsum, label="CDF of Average Inter-request Intervals")
ax1.plot(bins, y_med_cumsum, label="CDF of Median Inter-request Intervals")
ax1.set_xlabel("Time(s)")
ax1.set_ylabel("Distribution of request Intervals")

#labels = [str(x) for x in range(bins[-1]) if x%100==0]

ax1.grid()
ax1.legend(loc="lower right")

#plt.xticks(bins, labels, rotation='90')
plt.savefig('inter_arrival_cfd.png', dpi=300, bbox_inches='tight')


