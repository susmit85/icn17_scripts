import os
import sys
path = sys.argv[1]

file_l = []
for root, dirs, files in os.walk(path):
    if 'results' in root:
        file_l.extend([os.path.join(root, filename) for filename in files if 'cache' in filename])

filelist = sorted(file_l, key=lambda x: int(x.split("_")[-1].split('.')[0]))



for file_n in filelist:
    scheduledInterest = 0
    onInterest = 0
    onData = 0
    hopCount = 0
    max_hop_dir = {}
    with open(file_n, 'r') as f:
        print('Processing {}'.format(file_n))
        file_d = f.read().splitlines()
        for line in file_d:
            if 'Scheduling' in line:
                scheduledInterest += 1
            if 'OnInterest' in line:
                onInterest += 1
            if 'onData' in line:
                onData += 1
            if 'Hop' in line:
                split_line = line.split(",")
                nonce = int(split_line[4].split(" ")[-2])            
                data_nonce = int(split_line[5].split('/')[-1])
                hop_count = int(split_line[-1].strip().split()[-1]) if nonce == data_nonce else 1
                hopCount += hop_count
        print("Scheduled Interests {} onInterest {} onData {} hopCount {}".format(scheduledInterest, onInterest,
        onData, hopCount))


