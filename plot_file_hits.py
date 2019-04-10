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

x = range(len(hit_list))
y = sorted(hit_list)

fig = plt.figure()

ax2 = fig.add_subplot(111)

plt.gca().xaxis.set_major_locator(plt.NullLocator())

ax2.bar(x, y, .5, label="Number of Requests for each file")
ax2.set_xlabel("Individual Files")
ax2.set_ylabel("Number of Requests for files")

ax2.set_yscale('log')
ax2.grid()
#ax2.legend(loc="lower right")
ax2.legend()
plt.savefig('request_patterns.png', dpi=300)


