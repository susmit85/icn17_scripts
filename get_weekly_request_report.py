import csv
import sys
import numpy as np

time_list = []

with open(sys.argv[1], 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = '\t')
    for row in reader:
        try:
            client = row[5]
            time = int(row[9])
            time_list.append(time)

        except:
            print("Passing {}".format(row))
            pass

time_list.sort()
start_bin = time_list[0]
end_bin = time_list[-1]

print(start_bin, end_bin)
time_bins = [i for i in range(start_bin, end_bin, 3600*24*7)]
hist, bin_edges = np.histogram(time_list, time_bins)

sorted_hist = sorted(hist)
for i in range(-20,-1):
    print(sorted_hist[i], bin_edges[hist.tolist().index(sorted_hist[i])])
