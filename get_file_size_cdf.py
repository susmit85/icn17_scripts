import sys 
import csv
import operator
from collections import Counter
import matplotlib
matplotlib.use('Agg')
label_size = 12
matplotlib.rcParams['xtick.labelsize'] = label_size 
import matplotlib.pyplot as plt
import numpy as np


log = sys.argv[1]
file_dict = {}
with open(log, 'r') as f:
    reader = csv.reader(f, delimiter ='\t')
    for row in reader:
        filename = row[3]
        filesize = int(row[14])
        try:
            if filesize > file_dict[filename]:
                file_dict[filename] = filesize
        except KeyError:
            file_dict[filename] = filesize if filesize > 0 else 0

size_list = []
for key, val in file_dict.items():
    if int(val) > 0:
       size_list.append(int(val))
print("Total Requested Size = {}".format(sum(size_list)))

bins = [x*100000000 for x in range(31)]
counts, bin_edges = np.histogram(sorted(size_list), bins)

cdf = np.cumsum(counts)
total_counts = sum(counts)
cdf_list =[0]
cdf_list += [y/total_counts for y in cdf]
print(bins, cdf_list, np.percentile(sorted(size_list), 95))

fig = plt.figure()
ax1 = fig.add_subplot(111)
#plt.hist(sorted(size_list), bins)
ax1.plot(bin_edges, cdf_list, label="CDF of Object Sizes")

ax1.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
#x_tick_labels = [str(x/1000000.0)+" MB" for x in bins if (x/1000000.0)%200==0.0]
#ax1.set_xticks(bins)
#ax1.set_xticklabels(x_tick_labels, rotation='80')
fig.canvas.draw()
labels = ax1.get_xticklabels()
label_list = []
for label in labels:
    print(label.get_text()+" GB")
    label_list.append(label.get_text() + " GB")
ax1.set_xticklabels(label_list, rotation='80')    


plt.tick_params(axis='both', which='major', labelsize=16)
plt.tick_params(axis='both', which='minor', labelsize=12)

ax1.set_xlabel("Size of Requests", fontsize=16)
ax1.set_ylabel("Percentage of Requests", fontsize=16)

ax1.grid()
ax1.legend(loc="lower right", prop={'size': 16})
fig.tight_layout()
plt.savefig('file_size_cdf_successful.pdf', dpi=300)



