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
 #                  time_dict[start_time][filename][1] = filesize
                    time_dict[start_time][filename][2].append(user_name)

                else:
                    time_dict[start_time][filename] = [1, filesize, [user_name]]

        except:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

#plot duplicate requests on y axis, dot plot, number of unique users in z axis

#get things in lists, so that we can plot them

for time, dic in sorted(time_dict.items(), key=lambda t:t[0]):
#    for subkey, subval in dic.items():
#        print(subval[0], set(subval[2]))
    total_dup_req = 0
    total_users = 0
    unique_users = 0
    total_size_ip = 0
    total_size_ndn = 0
    #                    print(time, dic)
    for subkey, subval in dic.items():
#        print(subkey, subval)
        total_dup_req = int(subval[0])
        total_users = len(subval[2])
        unique_users = len(set(subval[2]))
        if unique_users > 1:
#            print(total_dup_req, unique_users)
            x.append(datetime.datetime.fromtimestamp(int(time)))
            y.append(total_dup_req)
            z.append(unique_users)

#print (len(x), len(y), len(z))

from pylab import figure, show, legend, ylabel

# create the general figure
fig1 = figure()
ax1 = fig1.add_subplot(111)
ax1.plot_date(x,y, "ro",rasterized=True)
plt.xlabel('Time (10 Minute Intervals)', size=20)
plt.ylabel("Total number of multi-user accesses", size=20)
ax1.set_yscale('log')
axes = plt.gca()
#axes.set_ylim([0,100])


ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
ax2.plot(x,z, color ="green")
axes = plt.gca()
#axes.set_ylim([0,500])
ax2.set_yscale('log')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ylabel("Number of Unique Users", size=20)
ax1.autoscale_view()
plt.legend()

fig1.autofmt_xdate()
fig1.savefig('dup_users.pdf', dpi=200)
#
#
#
#sys.exit(1)
#print("%s/%s" %(line_count, total_count))
#
##plot duplicate requests etc
##print datetime.datetime.fromtimestamp(int(line[0])/1000)
#fig, ax = plt.subplots()
##ax.set_yscale('log')
#ax.plot(x, y, label='Total Number of Duplicate Requests')
#ax.plot(x, z, label='Number of Unique Files Requested')
#ax.autoscale_view()
#plt.xlabel('Time (10 mins)')
#plt.ylabel('Data Requests')
#legend = ax.legend(loc='upper right', shadow=True)
#for label in legend.get_texts():
#    label.set_fontsize('x-small')
#
#fig.autofmt_xdate()
#plt.show()
#fig.savefig('requests.pdf', dpi=300)
#plt.close(fig)
