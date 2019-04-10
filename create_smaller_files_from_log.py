import csv
import sys

input_log = sys.argv[1]

ip_list = []
with open(input_log, 'r') as r:
    reader = csv.reader(r, delimiter='\t')
    for row in reader:
        ip = row[5]
        ip_list.append(ip)
        try:
            filename = "/raid/ndnSIM_final/ns-3/src/ndnSIM/examples/llnl/data/" + ip + ".small.txt"
            with open(filename, 'a') as f:
                f.write("\t".join(row)+'\n')
        except:
            print("Error processing line ", row)
            pass

print(len(set(ip_list)))

    
