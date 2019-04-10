import re
import sys
import csv
import datetime
import numpy as np
import traceback

with open(sys.argv[1], 'r') as f:
#    pass
    reader = csv.reader(f, delimiter ='\t')
    line_count = 0
    total_count = 0
    x = []
    y = []
    z = []
    ip_size = []
    ndn_size = []
    start_time = 0
    end_time = 0
    time_dict = {}
    
    #create the interval buckets
    with open('filter_apr.txt', 'w') as dest:
      writer = csv.writer(dest, delimiter ='\t')
      for line in reader:
        if 1459468800 <= int(line[9]) <= 1461974400:
        #if 1461456000 <= int(line[9]) <= 1461974400:
            writer.writerow(line)
