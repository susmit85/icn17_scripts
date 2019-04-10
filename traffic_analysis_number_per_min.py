import sys 
import csv
import operator
from collections import Counter
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt
import numpy as np
import traceback
import datetime


log = sys.argv[1]

time_list = []
traffic_volume = [] 
request_volume = [] 
with open(log, 'r') as f:
    reader = f.read()
    for row in reader.split('\n'):
        split_row = row.split('\t')
        try:
            request_size = int(split_row[14])
            timestamp = int(split_row[9])
            transfer_size = int(split_row[15])
            time_list.append(timestamp)
            request_volume.append(request_size)
            traffic_volume.append(transfer_size)
        except:
            print("Ignoring line {} trace {}".format(row, traceback.format_exc()))
            pass

time_list.sort()
start_time = time_list[0]
end_time = time_list[-1]
total_vol = []
xfer_vol = []
bins = [x for x in range(start_time, end_time, 600)]
time_bins = [datetime.datetime.fromtimestamp(int(time)) for time in bins]

hist_request_count, bin_edges_count = np.histogram(sorted(time_list), bins)
cum_hist_request_count = np.cumsum(hist_request_count)
for i in range(1, len(cum_hist_request_count)):
    lower_index = cum_hist_request_count[i-1]
    upper_index = cum_hist_request_count[i]
    total_vol.append(sum(request_volume[lower_index:upper_index])/1000000000)
    xfer_vol.append(sum(traffic_volume[lower_index:upper_index])/1000000000)


print(len(bins), len(total_vol), len(xfer_vol))

fig = plt.figure()

ax2 = fig.add_subplot(111)
ax2.plot(time_bins[2:], xfer_vol, color='blue')
ax2.set_xlabel("Time(10 minute intervals)")
ax2.set_ylabel("Cumulative volume of requests(GB)")
ax2.grid()
#ax2.set_yscale('log')
fig.autofmt_xdate()


plt.savefig('xfer_volume_per_month_started.png', dpi=300)


