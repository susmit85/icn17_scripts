import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
import datetime
from operator import truediv
import csv

time_series = []
retrieved = []
requested = []
total_retrieved = []
total_requested = []
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        time,flag,req_size,xfer_size = int(line[8]), line[10], int(line[14]), int(line[15])
        time_series.append(time)
        retrieved.append((xfer_size if xfer_size > 0 and req_size > 0 else 0))
        requested.append((req_size if req_size > 0 else 0))

ticks = np.arange(1326440142,1458114218,600)

time_bins = np.array(ticks)
success_ratio_list = []

succ_ratio_hist, success_ratio_bin_edges = np.histogram(sorted(time_series), bins = time_bins)
start_index = 0
end_index = 0
for item in succ_ratio_hist:
 #   print(item)
    end_index = start_index + item
    total_ret = sum(retrieved[start_index:end_index])/1000000000.0
    total_req = sum(requested[start_index:end_index])/1000000000.0
    try:
        success_ratio_list.append(total_ret*100.0/total_req)
        total_retrieved.append(total_ret)
        total_requested.append(total_req)
    except ZeroDivisionError:
        success_ratio_list.append(0)
        total_retrieved.append(0)
        total_requested.append(0)
    start_index = end_index


reversed_total_retrieved = [(-i) for i in total_retrieved]
fig = plt.figure()

ax2 = fig.add_subplot(111)
ax2.plot(time_bins[1:], total_requested,  color="red")
ax2.plot(time_bins[1:], reversed_total_retrieved,  color="blue")
ax2.set_ylabel("Volume of Data (GB)")
ax2.set_xlabel("Time(10 minute bins)")

for ax in [ax2]:
  start, end = ax.get_xlim()
#  print(start, end)
  ax.legend(loc='upper right')
  ax.grid()
#  y_ticks = [-10000, -5000, 0, 5000, 10000]
#  ax.set_yticks(y_ticks)
#  ax.set_yticklabels([10000, 5000, 0, 5000, 10000])


  #set 6mo ticks
  x_ticks = np.arange(time_bins[0], time_bins[-1], 2629743*6)

  print(x_ticks[0], x_ticks[-1])
  ax.set_xticks(x_ticks)
  ax.set_xticklabels(
    [datetime.date.fromtimestamp(time) for time in x_ticks]
  )

  for tick in ax.xaxis.get_major_ticks():
      tick.label.set_fontsize(9) 
      # specify integer or one of preset strings, e.g.
      tick.label.set_fontsize('x-small') 
      tick.label.set_rotation('vertical')

  fig.autofmt_xdate()  

fig.savefig("requested_retrieved_volume.png", dpi=300)
