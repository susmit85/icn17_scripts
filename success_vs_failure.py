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
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
#       print(line)
        time,flag,req_size,xfer_size = int(line[8]), line[10], int(line[14]), int(line[15])
#        print(time,flag,req_size,xfer_size)
        if flag == 'f' or req_size > xfer_size or req_size < 0:
            failure.append(time)
        else:
            success.append(time)


#sys.exit(1)

fig = plt.figure()


ax1 = fig.add_subplot(111)

ticks = np.arange(1326440142,1458114218,600)
time_bins = np.array(ticks)
#axes = plt.gca()
#axes.set_ylim([-12000,12000])
#axes.set_xlim([1326440142,1458114218])
#fig.text(0.5,0.01,'Time, Interval = 10 Minutes', ha="center")
#fig.text(0.01,0.5,'Number of Cumulative requests at server', va="center", rotation='vertical')



#ax1.hist(sorted(ip_times), bins=time_bins, histtype = 'step', color="blue", label="IP")
#ax1.hist(sorted(ndn_times), bins=time_bins, histtype = 'step', color="red", label="NDN")

success_hist, success_bins_edges = np.histogram(sorted(success), bins = time_bins)
failure_hist, failure_bin_edges  = np.histogram(sorted(failure), bins = time_bins)
failure_hist = [(-i) for i in failure_hist]
ax1.plot(time_bins[1:], success_hist, 'r-', color="blue", label="Successful Requests")
ax1.plot(time_bins[1:], failure_hist, 'r-', color="red", label="Failed Requests")

ax1.set_ylim([-12000,12000])
#ax2.set_ylim([0,12000])
#ax3.set_ylim([0,100])
ax1.set_ylabel("Number of Requests at Producer")
ax1.set_xlabel("Time(10 minute bins)")

for ax in [ax1]:
  start, end = ax.get_xlim()
  print(start, end)
  ax.legend(loc='upper right')
  ax.grid()
  y_ticks = [-10000, -5000, 0, 5000, 10000]
  ax.set_yticks(y_ticks)
  ax.set_yticklabels([10000, 5000, 0, 5000, 10000])


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

fig.savefig("success_vs_failure.png", dpi=300)
