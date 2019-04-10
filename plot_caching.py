import re
import sys
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import numpy as np
import traceback

x_axis = [1,2,3,4,5,10,20]

y_axis_dict = { 60 : [59.174057649667404, 70.3048780487805, 74.08536585365853, 77.86031042128603, 80.16629711751663,
91.18070953436808, 94.78381374722838], 300 : [33.58112475759535, 46.05688429217841, 51.92307692307692,
57.51454427925016, 61.71622495151907, 76.6645119586296, 85.58500323206205], 600: [22.90927521540801, 34.972123669538774,
40.42067916877851, 45.99594526102382, 50.0, 65.78813988849468, 78.53522554485555], 1200: [15.086887835703001, 24.091627172195892, 29.739336492890995, 34.241706161137444, 37.83570300157978, 52.68562401263823,
68.56240126382306], 1800: [11.190965092402465, 18.737166324435318, 23.562628336755647, 28.28542094455852,
32.08418891170431, 45.379876796714576, 60.831622176591374], 30: [68.04049907956637,
77.39824094906933, 79.92772891525193, 82.60380445898957, 84.23331287925275, 94.41603599918184, 96.703484011727],
10:[78.442663995994, 84.41780317535127, 85.94656690918731, 87.37518041768536, 88.36784588647677, 97.4741524050782,
98.51836578397007]}


fig, ax = plt.subplots()

ax.set_ylim(ymin=0)

fig, ax = plt.subplots()
#ax.set_yscale('symlog')
#ax.set_yscale('log')
#ax.set_ylim(ymin=0)
#ax.plot(x, ip_size_arr, label='Total IP bandwidth Requested')
#x.plot(x, ndn_size_arr, label='NDN Cache Size vs (%) Requests Aggregated')

#ax.plot(x, xfer_size_arr, label='Total Data Served ')
#ax.plot(x, ip_ndn_frac, label='NDN bandwidth savings')



#plot
for key, val in sorted(y_axis_dict.items(), key=lambda t:t[0]):
    ax.plot(x_axis, val, label= 'Aggregation Interval = %s secs' %(key))
ax.autoscale_view()
plt.xlabel('Cache Size(TB)')
plt.ylabel('Percentage of Requests Aggregated')
plt.xticks(x_axis)
legend = ax.legend(loc='lower right', shadow=True)
for label in legend.get_texts():
    label.set_fontsize('x-small')

fig.autofmt_xdate()
plt.show()
plt.grid()
fig.savefig('cache_size_vs_aggr_comp.pdf', dpi=300)
plt.close(fig)



