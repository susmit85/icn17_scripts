import csv
import sys
import numpy as np

client_throughput = {}
with open(sys.argv[1], 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = '\t')
    for row in reader:
        try:
            client = row[5]
            time = int(row[11])
            xfer_size = row[-1]
            bandwidth = int(xfer_size)/(time*1000)
            if client in client_throughput:
                client_throughput[client].append(bandwidth)
            else:
                client_throughput[client] = [bandwidth]
        except:
            print("Passing {}".format(row))
            pass

print(client_throughput)            

for key, value in client_throughput.items():
    mean_throughput = np.mean(value)
    print("Client = {:s}, Throughput = {:.2f} Kbps".format(key, mean_throughput))
