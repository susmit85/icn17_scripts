import re
import sys
import csv
import matplotlib
import datetime
import numpy as np
import traceback

with open(sys.argv[1], 'r') as f:
#    pass
    reader = csv.reader(f, delimiter ='\t')
   
    max_size = 0
    min_size = 0
    size_arr = []
    #create the interval buckets
    for line in reader:
        size_l =  int(line[-2])
        size_arr.append(size_l)

print(np.amin(size_arr), np.amax(size_arr), np.mean(size_arr))
