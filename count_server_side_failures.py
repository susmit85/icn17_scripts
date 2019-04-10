import csv
import sys

with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        success = row[10]
        if success == 'f':
            data_size = int(row[14])
            xfer_size = int(row[15])
            print(data_size, xfer_size)






