import re
import sys
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
    for line in reader:
        total_count += 1
        if total_count == 1:
            start_time = int(line[9])
            interval_end = start_time + 600
            user_name = line[1]
        try:
            user_name = line[1]
            timestamp = int(line[9])
            filename = line[3]
            filesize = line[14]
            line_count += 1
#            print(timestamp, filename, interval_end)

            if timestamp >= interval_end:
                start_time = int(line[9])
                interval_end = start_time + 600


            #timestamp not present, create an entry
            if start_time not in time_dict:
                time_dict[start_time] = {filename:[1,filesize,[user_name]]}


            #time stamp exists
            else:
                if filename in time_dict[start_time]:
                    time_dict[start_time][filename][0] += 1
                    time_dict[start_time][filename][1] = filesize
                    time_dict[start_time][filename][2].append(user_name)

                else:
                    time_dict[start_time][filename] = [1, filesize, [user_name]]

        except:
            traceback.print_exc(file=sys.stdout)


#compare ndn and IP bandwidth
for time, dic in sorted(time_dict.items(), key=lambda t:t[0]):
    total_dup_req = 0
    total_users = 0
    total_size_ip = 0
    total_size_ndn = 0
    #                    print(time, dic)
    for subkey, subval in dic.items():
     #   print(subkey, subval)
        total_dup_req = int(subval[0])
#        total_users += len(subval[2])
#   print("Time = %s, Total Requests = %s, Num_files = %s, total_users = %s" %(time, (total_dup_req), len(dic), total_users))
        total_size_ndn += float(subval[1])
#        print(subkey, subval)
    x.append(datetime.datetime.fromtimestamp(int(time)))
    y.append(total_size_ndn)
    z.append(total_size_ndn/2)


#print datetime.datetime.fromtimestamp(int(line[0])/1000)
fig, ax = plt.subplots()
#ax.set_yscale('log')
ax.plot_date(x, y, 'b-', rasterized=True, label='NDN bandwidth requirement')#, label='Total Number of Duplicate Requests')
ax.plot_date(x, z, 'r-', rasterized=True, label='Single node NDN Bandwidth Requirement with load balancing')#, label='Total Number of Duplicate Requests')
ax.autoscale_view()
plt.xlabel('Time (10 mins)')
plt.ylabel('Aggregate Bandwidth Requirement (GB)')
legend = ax.legend(loc='upper right', shadow=True)
for label in legend.get_texts():
    label.set_fontsize('x-small')

fig.autofmt_xdate()
#plt.show()
fig.savefig('multi_node_ndn.pdf', dpi=100)
plt.close(fig)


