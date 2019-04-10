import re
import sys
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import numpy as np
import traceback
#works with the plot_caching.py
with open(sys.argv[1], 'r') as f:
#    pass
    reader = csv.reader(f, delimiter ='\t')
    line_count = 0
    total_count = 0
    x = []
    y = []
    z = []
    ip_size_arr = []
    ndn_size_arr = []
    xfer_size_arr = []
    ip_ndn_frac = []
    unique_users_arr = []
    start_time = 0
    end_time = 0
    time_dict = {}
    forward_interval = 10
    
    #create the interval buckets
    for line in reader:
        total_count += 1
        if total_count == 1:
            start_time = int(line[9])
            interval_end = start_time + forward_interval
            user_name = line[1]
        try:
            user_name = line[1]
            timestamp = int(line[9])
            filename = line[3]
            filesize = line[14]
            xfer_size = line[15]
            line_count += 1
#            print(timestamp, filename, interval_end)

            if timestamp >= interval_end:
                start_time = int(line[9])
                interval_end = start_time + forward_interval


            #timestamp not present, create an entry
            if start_time not in time_dict:
                time_dict[start_time] = {filename:[1,filesize, xfer_size, [user_name]]}


            #time stamp exists
            else:
                if filename in time_dict[start_time]:
                    time_dict[start_time][filename][0] += 1
                    time_dict[start_time][filename][1] = filesize
                    time_dict[start_time][filename][2] = xfer_size
                    time_dict[start_time][filename][3].append(user_name)

                else:
                    time_dict[start_time][filename] = [1, filesize, xfer_size, [user_name]]

        except:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)
#get things in lists, so that we can plot them

count = 0
for time, dic in sorted(time_dict.items(), key=lambda t:t[0]):
#    print(time, dic)
#    if count == 10:
#        sys.exit(1)
    total_dup_req = 0
    total_users = 0
    total_xfer_size = 0
    total_size_ip = 0
    total_size_ndn = 0
    unique_users = 0
    #                    print(time, dic)
#for each file in the time period
    for subkey, subval in dic.items():
#        print(subkey, subval)
        total_dup_req = int(subval[0])
        file_size = int(subval[1])
        xfer_size = int(subval[2])
        total_users = len(subval[3])

        if int(subval[1]) >= 1:
            total_size_ip += (total_dup_req * file_size)
            total_size_ndn += file_size
            total_xfer_size += xfer_size

#    print("Time = %s, Total Requests = %s, total_users = %s total_size=%s xfer_size=%s" %(time, (total_dup_req),
#    total_users, file_size, xfer_size))
#    x.append(datetime.datetime.fromtimestamp(int(time)))
#bytes to GB
#   ip_size_arr.append(total_size_ip/1000000000)
    try:
       #ip_ndn_frac.append(((total_size_ip-total_size_ndn)/total_size_ip)*100)
       x.append(datetime.datetime.fromtimestamp(int(time)))
       ndn_size_arr.append(total_size_ndn/1000000000.0)
    except:
        pass
#   xfer_size_arr.append(total_xfer_size/1000000000)


#print("%s/%s" %(line_count, total_count))


#plot the bandwidth pics
less_than_tb = (sum(i < 1 for i in ndn_size_arr)*100.0)/len(ndn_size_arr)
less_than_2tb = (sum(i < 2 for i in ndn_size_arr)*100.0)/len(ndn_size_arr)
less_than_3tb = (sum(i < 3 for i in ndn_size_arr)*100.0)/len(ndn_size_arr)
less_than_4tb = (sum(i < 4 for i in ndn_size_arr)*100.0)/len(ndn_size_arr)
less_than_5tb = (sum(i < 5 for i in ndn_size_arr)*100.0)/len(ndn_size_arr)
less_than_10tb = (sum(i < 10 for i in ndn_size_arr)*100.0)/len(ndn_size_arr)
less_than_20tb = (sum(i < 20 for i in ndn_size_arr)*100.0)/len(ndn_size_arr)
total_size = (sum(i for i in ndn_size_arr))
#
x_cache_size = [1, 2, 3, 4, 5, 10, 20]
y_cache_saving = [less_than_tb, less_than_2tb, less_than_3tb, less_than_4tb, less_than_5tb, less_than_10tb,
less_than_20tb]
#
#
print(x_cache_size, y_cache_saving)
sys.exit(1)
#ax.set_ylim(ymin=0)
fig, ax = plt.subplots()
#ax.set_yscale('symlog')
#ax.set_yscale('log')
#ax.set_ylim(ymin=0)
#ax.plot(x, ip_size_arr, label='Total IP bandwidth Requested')
#x.plot(x, ndn_size_arr, label='NDN Cache Size vs (%) Requests Aggregated')

#ax.plot(x, xfer_size_arr, label='Total Data Served ')
#ax.plot(x, ip_ndn_frac, label='NDN bandwidth savings')



#plot 
ax.plot(x_cache_size, y_cache_saving, label='NDN Cache Size vs (%) Requests Aggregated')
ax.autoscale_view()
plt.xlabel('Cache Size(TB)')
plt.ylabel('Percentage of Requests Aggregated')
legend = ax.legend(loc='upper right', shadow=True)
for label in legend.get_texts():
    label.set_fontsize('x-small')

fig.autofmt_xdate()
plt.show()
fig.savefig('cache_size_vs_aggr.pdf', dpi=300)
plt.close(fig)


