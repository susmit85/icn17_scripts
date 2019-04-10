import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
import datetime
from operator import truediv
import csv

total_data_dict = {}
successful_req = 0
successful_req_count = 0
unique_req_count = 0

with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
#       print(line)
        time,filename,req_size,xfer_size = int(line[8]), line[3], int(line[14]), int(line[15])
        if req_size == xfer_size and req_size > 0:
            successful_req += req_size
            successful_req_count += 1

            if filename in total_data_dict:
                if total_data_dict[filename] < req_size:
                    total_data_dict[filename] = req_size
                    unique_req_count += 1
                else:
                    pass
            else:
                total_data_dict[filename] = req_size
                unique_req_count += 1

print(sum(total_data_dict.values()), unique_req_count, successful_req, successful_req_count)




