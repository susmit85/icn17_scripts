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
 
        split_row = row.split('\t')
        filesize = int(split_row[14])
        transfer_size = int(split_row[15])
        try:
            if filesize > 1:
               client_dict[ip_addr][0] += filesize
               client_dict[ip_addr][1] += transfer_size
        except KeyError:
            client_dict[ip_addr] = [filesize if filesize > 0 else 0, transfer_size if transfer_size > 0 else 0]
print(client_dict)            


request_size = []
transfer_size = []

bins = [x*10000000000 for x in range(50)]
for key, val in client_dict.items():
    request_size.append(val[0])
    transfer_size.append(val[1])
    


hist_req, bin_edges_req= np.histogram(sorted(request_size), bins)
hist_tran, bin_edges_tran= np.histogram(sorted(transfer_size), bins)

sum_hist_req = sum(hist_req)
percent_reqs = [i/sum_hist_req for i in hist_req]

cdf_req = [0]
cdf_req.extend(np.cumsum(percent_reqs))

print(hist_req, bin_edges_req, cdf_req)

plot_bins = [x for x in bins if bins.index(x)%5 == 0]
labels = [str(x/10000000000) + "TB" for x in plot_bins]
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(bin_edges_req, cdf_req, label="CDF of Request Sizes")
ax1.set_xlabel("Cumulative Request Sizes at Clients")
ax1.set_ylabel("CDF of Request Size")



ax1.grid()
ax1.legend(loc="lower right")

print(plot_bins, labels)
plt.xticks(plot_bins, labels, rotation='45')
plt.savefig('req_size_cfd.png', dpi=300, bbox_inches='tight')


