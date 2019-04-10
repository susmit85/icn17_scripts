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
 
        success = True
        split_row = row.split('\t')
        filesize = int(split_row[14])
        transfer_size = int(split_row[15])
        if filesize > transfer_size or filesize == -1:
            success = False
        try:
            if success:
                client_dict[ip_addr][0] += 1
            else:
                client_dict[ip_addr][1] += 1
        except KeyError:
            if success:
                client_dict[ip_addr] = [1,0]
            else:
                client_dict[ip_addr] = [0,1]
            
            
#print(client_dict)
#sorted_file_list = sorted(file_dict.items(), key=operator.itemgetter(1))
failure_ratio = [0]
success_ratio = [0]

for key, val in client_dict.items():
    failure_ratio.append(val[1]/(val[0]+val[1]))
    success_ratio.append(val[0]/(val[0]+val[1]))
#print(failure_ratio, success_ratio, len(success_ratio), len(failure_ratio))


bins = [x*0.10 for x in range(11)]

hist_fail, bin_edges_fail = np.histogram(sorted(failure_ratio), bins)
hist_succ, bin_edges_succ = np.histogram(sorted(success_ratio), bins)

x_axis_fail = [0]
x_axis_fail.extend(hist_fail)

x_axis_succ = [0]
x_axis_succ.extend(hist_succ)
#print(x_axis_fail, bins)

cdf_fail = np.cumsum(x_axis_fail)
cdf_succ = np.cumsum(x_axis_succ)

fig = plt.figure()
ax1 = fig.add_subplot(211)

ax1.plot(cdf_fail, bin_edges_fail, label="CDF of Partial Transfers")
ax1.set_xlabel("Number of Clients")
ax1.set_ylabel("CFD of Parial Transfers")
ax1.set_yticks(bins)

ax1.grid()
ax1.legend(loc="lower right")

ax2 = fig.add_subplot(212)

ax2.plot(cdf_succ, bin_edges_succ, label="CDF of Success")
ax2.set_xlabel("Number of Clients")
ax2.set_ylabel("CDF of Success")
ax2.set_yticks(bins)

ax2.grid()
ax2.legend(loc="lower right")
plt.savefig('failure_cfd.png', dpi=300)

#
##ax2 = fig.add_subplot(212)
#
##ax2.plot(sorted(hit_list), label="Number of Requests for each file")
##ax2.set_xlabel("Request Frequency")
##ax2.set_ylabel("Fraction of Requests")
#
##ax2.grid()
##ax2.legend(loc="lower right")
##plt.savefig('request_patterns.png', dpi=300)
#
