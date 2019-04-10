import sys 
import csv
import operator
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

log = sys.argv[1]
file_dict = {}
with open(log, 'r') as f:
    reader = csv.reader(f, delimiter ='\t')

    for row in reader:
        filename = row[3]
        try:
            file_dict[filename] += 1
        except KeyError:
            file_dict[filename] = 1

#sorted_file_list = sorted(file_dict.items(), key=operator.itemgetter(1))
hit_list = []

for key, val in file_dict.items():
    hit_list.append(val)

#calculate cdf

x_axis = [0]
y_axis = [0]
total = len(hit_list)
print(total)
prev_percentage = 0.0

for item in sorted(set(hit_list)):
    percentage = hit_list.count(item)/total
    cdf = prev_percentage + percentage
    x_axis.append(item)
    y_axis.append(cdf)
#   print(item, hit_list.count(item), prev_percentage, cdf)
    prev_percentage = cdf

print(x_axis[0:10], x_axis[-10:-1], y_axis[0:10], y_axis[-10:-1])

fig = plt.figure()
ax1 = fig.add_subplot(111)

#line1 = ax1.plot(x_axis, y_axis, 'b-', label ='aa')

#start, end = ax1.get_xlim()
#ax1.xaxis.set_ticks(np.arange(start, end, 10))

ax1.plot(x_axis[0:100], y_axis[0:100], 'r-', label="CDF of Request Frequency for transfers that started\n Max requests\
for one file 425,295")
ax1.set_xlabel("Request Frequency")
ax1.set_ylabel("Fraction of Requests")

ax1.grid()
ax1.legend(loc="lower right")
plt.savefig('request_number_started.png', dpi=300)


#ax2 = fig.add_subplot(212)

#ax2.plot(sorted(hit_list), label="Number of Requests for each file")
#ax2.set_xlabel("Request Frequency")
#ax2.set_ylabel("Fraction of Requests")

#ax2.grid()
#ax2.legend(loc="lower right")
#plt.savefig('request_patterns.png', dpi=300)


