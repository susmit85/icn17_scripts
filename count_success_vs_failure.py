import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
import datetime
from operator import truediv
import csv


success =0
failure = 0

with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        time,flag,req_size,xfer_size = int(line[8]), line[10], int(line[14]), int(line[15])
        success += 1 if xfer_size == req_size and req_size > 0 else 0
        failure += 1 if req_size < 0 or xfer_size < 0 or req_size > xfer_size else 0
print(success, failure)

