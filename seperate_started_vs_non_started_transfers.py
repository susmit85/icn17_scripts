import csv
import sys

started = 0
didnot_start = 0
with open(sys.argv[1], 'r') as f, open("../LLNL_access_log_started.csv", 'w') as s,\
open("../LLNL_access_log_did_not_start.csv", 'w') as d:
        
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        success = row[10]
#       if success == 'f':
        data_size = int(row[14])
        xfer_size = int(row[15])
        if xfer_size <= 0:
            didnot_start += 1
            d.write("\t".join(row)+'\n')
            
        else:
            started += 1
            s.write("\t".join(row)+'\n')

print(started, didnot_start)





