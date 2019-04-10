import re
import sys
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import numpy as np
import traceback

#    pass
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter ='\t')
    line_count = 0
    lines = []
    for line in reader:
        lines.append(line)

forward_interval = [10, 30, 60, 300, 600, 1200, 1800]
time_dict_arr = {}
for interval in forward_interval:
    x = []
    y = []
    z = []
    ip_size_arr = []
    ndn_size_arr = []
    xfer_size_arr = []
    ip_ndn_frac = []
    unique_users_arr = []
    end_time = 0
    
#create the interval buckets
    time_dict = {}
    total_count = 0
    start_time = 0
    for line in lines:
        total_count += 1
#        if total_count == 2000:
#            break
        if total_count == 1:
            start_time = int(line[9])
            interval_end = start_time + interval
            user_name = line[1]
        try:
            timestamp = int(line[9])
            filename = line[3]
            filesize = line[14]
            xfer_size = line[15]
            line_count += 1
#            print(timestamp, filename, interval_end)

            if timestamp >= interval_end:
                start_time = int(line[9])
                interval_end = start_time + interval


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
    time_dict_arr[interval] = time_dict
#    print (interval, len(time_dict), len(time_dict_arr[interval]), len(time_dict_arr))

#sys.exit(1)
x_arrs = {10:[], 30:[], 60:[], 300:[], 600:[], 1200:[], 1800:[]}
ndn_arrs = {10:[], 30:[], 60:[], 300:[], 600:[], 1200:[], 1800:[]}
#print(time_dict_arr)
for interval, time_dict in sorted(time_dict_arr.items(), key=lambda t:t[0]):
    ndn_size_arr = []
    x = []
 #  print("I:T",interval, time_dict)
    for time, dic in sorted(time_dict.items(), key=lambda t:t[0]):
#        x = []
    #    ndn_size_arr = []
        total_dup_req = 0
        total_users = 0
        total_xfer_size = 0
        total_size_ip = 0
        total_size_ndn = 0
        unique_users = 0
#        print(time, dic)
#for each file in the time period
        for subkey, subval in dic.items():
#            print("SS",subkey, subval)
#            total_dup_req = int(subval[0])
            file_size = int(subval[1])
#            xfer_size = int(subval[2])
#            total_users = len(subval[3])

            if int(subval[1]) >= 1:
#                total_size_ip += (total_dup_req * file_size)
                total_size_ndn += file_size
#                total_xfer_size += xfer_size
#                print(total_size_ndn)
#
                try:
                   x.append(datetime.datetime.fromtimestamp(int(time)))
                   ndn_size_arr.append(total_size_ndn/1000000000.0)
#                   print(len(x), len(ndn_size_arr))
                except:
                    print("Err")
                    pass
#        print("x=",x)
    x_arrs[interval].append(x)
    ndn_arrs[interval].append(ndn_size_arr)

#sys.exit(1)              
#print (len(x_arrs), len(ndn_arrs))
#print (x_arrs[0], ndn_arrs[0])
#print (len(x_arrs[1]), len(ndn_arrs[1]))
#print (len(x_arrs[2]), len(ndn_arrs[2]))
#print (len(x_arrs[3]), len(ndn_arrs[3]))
#print (len(x_arrs[4]), len(ndn_arrs[4]))
    
#fig, ax = plt.subplots()
#ax.set_ylim(ymin=0)
#ax.set_yscale('symlog')
#ax.set_yscale('log')
#ax.set_ylim(ymin=0)
#ax.plot(x, ip_size_arr, label='Total IP bandwidth Requested')
#x.plot(x, ndn_size_arr, label='NDN Cache Size vs (%) Requests Aggregated')

#ax.plot(x, xfer_size_arr, label='Total Data Served ')
#ax.plot(x, ip_ndn_frac, label='NDN bandwidth savings')



#plot 
#print(x_arrs[600][0], ndn_arrs[600][0])

f, axarr = plt.subplots(3, 3)
axarr[0,0].plot(x_arrs[10][0], ndn_arrs[10][0], label='Data Size over 10 Seconds')
axarr[0,1].plot(x_arrs[30][0], ndn_arrs[30][0], label='Data Size over 30 Seconds')
axarr[0,2].plot(x_arrs[60][0], ndn_arrs[60][0], label='Data Size over 60 Seconds')
axarr[1,0].plot(x_arrs[300][0], ndn_arrs[300][0], label='Data Size over 300 Seconds')
axarr[1,1].plot(x_arrs[600][0], ndn_arrs[600][0], label='Data Size over 600 Seconds')
axarr[1,2].plot(x_arrs[1200][0], ndn_arrs[1200][0], label='Data Size over 1200 Seconds')
axarr[2,0].plot(x_arrs[1800][0], ndn_arrs[1800][0], label='Data Size over 1800 Seconds')
#ax.autoscale_view()

plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)


#plt.ylabel('Aggregate Size of De-duplicated Requests')
#legend = ax.legend(loc='upper right', shadow=True)
#for label in legend.get_texts():
#    label.set_fontsize('x-small')

#fig.autofmt_xdate()
#plt.show()
f.savefig('data_size_vs_aggr1.pdf', dpi=300)
plt.close(f)


