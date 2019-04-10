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
    w = []
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
        #print(subkey, subval[0], subval[1])
        total_dup_req = int(subval[0])
#        total_users += len(subval[2])
#   print("Time = %s, Total Requests = %s, Num_files = %s, total_users = %s" %(time, (total_dup_req), len(dic), total_users))
        if int(subval[1]) > 0:
            total_size_ip += (int(total_dup_req) * float(subval[1])*8)/(1000000000*600)
            total_size_ndn += (float(subval[1])*8)/(1000000000*600)
#        print(subkey, subval)
#negative means failed
    x.append(datetime.datetime.fromtimestamp(int(time)))
    y.append(total_size_ndn)
    z.append(total_size_ip)


#print datetime.datetime.fromtimestamp(int(line[0])/1000)
fig, ax = plt.subplots()
#ax.set_yscale('log')
ax.plot_date(x, z, 'b-', rasterized=True, label='Bandwidth requirement in IP')#, label='Total Number of Duplicate Requests')
ax.plot_date(x, y, 'r-', rasterized=True, label='NDN with 100% aggregated requests')#, label='Total Number of Duplicate Requests')
ax.autoscale_view()
plt.xlabel('Time')
plt.ylabel('Maximum Required Bandwidth (Gbps)')
legend = ax.legend(loc='upper right', shadow=True)
for label in legend.get_texts():
    label.set_fontsize('large')

fig.autofmt_xdate()
#plt.show()
fig.savefig('climate_bw_savings_month_gbps.pdf', dpi=100, bbox_inches = 'tight')
plt.close(fig)
sys.exit(1)



#get things in lists, so that we can plot them

for time, dic in sorted(time_dict.items(), key=lambda t:t[0]):
    total_dup_req = 0
    total_users = 0
    total_size_ip = 0
    total_size_ndn = 0
    #                    print(time, dic)
    for subkey, subval in dic.items():
     #   print(subkey, subval)
        total_dup_req += int(subval[0])
#        total_users += len(subval[2])
#   print("Time = %s, Total Requests = %s, Num_files = %s, total_users = %s" %(time, (total_dup_req), len(dic), total_users))
        total_size_ip = total_dup_req * subval[1] 
        total_size_ndn = subval[1] 
#        print(subkey, subval)
        if(int(subval[0]) > -1):
            x.append(datetime.datetime.fromtimestamp(int(time)))
            y.append(int(subval[0]))


#print datetime.datetime.fromtimestamp(int(line[0])/1000)
fig, ax = plt.subplots()
ax.set_yscale('log')
ax.plot_date(x, y, 'ro', rasterized=True)#, label='Total Number of Duplicate Requests')
#ax.plot(x, z, label='Number of Unique Files Requested')
ax.autoscale_view()
plt.xlabel('Time (10 mins)')
plt.ylabel('Duplicate Data Requests')
#legend = ax.legend(loc='upper right', shadow=True)
#for label in legend.get_texts():
#    label.set_fontsize('x-small')

fig.autofmt_xdate()
#plt.show()
fig.savefig('climate_duplicate_data_requests.pdf', dpi=100)
plt.close(fig)
sys.exit(1)


#get things in lists, so that we can plot them

for time, dic in sorted(time_dict.items(), key=lambda t:t[0]):
    total_dup_req = 0
    total_users = 0
    total_size_ip = 0
    total_size_ndn = 0
    #                    print(time, dic)
    for subkey, subval in dic.items():
     #   print(subkey, subval)
        total_dup_req += float(subval[0])
        total_users += len(subval[2])
    print("Time = %s, Total Requests = %s, Num_files = %s, total_users = %s" %(time, (total_dup_req), len(dic), total_users))
    total_size_ip = total_dup_req * subval[1]/1000000000.0
    total_size_ndn = subval[1]/1000000000
    x.append(datetime.datetime.fromtimestamp(int(time)))
    y.append(total_dup_req)
    ip_size.append(total_size_ip)
    ndn_size.append(total_size_ndn)
    z.append(len(dic))


print("%s/%s" %(line_count, total_count))


#print datetime.datetime.fromtimestamp(int(line[0])/1000)
fig, ax = plt.subplots()
ax.set_yscale('log')
ax.plot_date(x, y)#, label='Total Number of Duplicate Requests')
#ax.plot(x, z, label='Number of Unique Files Requested')
ax.autoscale_view()
plt.xlabel('Time (10 mins)')
plt.ylabel('Duplicate Data Requests')
#legend = ax.legend(loc='upper right', shadow=True)
#for label in legend.get_texts():
#    label.set_fontsize('x-small')

fig.autofmt_xdate()
#plt.show()
fig.savefig('climate_duplicate_data_requests.pdf', dpi=300)
plt.close(fig)
sys.exit(1)

#plot unique data requests vs time
#print datetime.datetime.fromtimestamp(int(line[0])/1000)
fig, ax = plt.subplots()
ax.set_yscale('log')
ax.plot(x, y, label='Total Number of Duplicate Requests')
ax.plot(x, z, label='Number of Unique Files Requested')
ax.autoscale_view()
plt.xlabel('Time (10 mins)')
plt.ylabel('Duplicate Data Requests')
legend = ax.legend(loc='upper right', shadow=True)
for label in legend.get_texts():
    label.set_fontsize('x-small')

fig.autofmt_xdate()
#plt.show()
fig.savefig('a.pdf', dpi=300)
plt.close(fig)
sys.exit(1)

#
#plot the bandwidth pics

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.plot(x, ip_size, label='Total IP bandwidth Required')
ax.plot(x, ndn_size, label='Total NDN Bandwidth Requested')
ax.autoscale_view()
plt.xlabel('Time (10 mins)')
plt.ylabel('Required Bandwidth')
legend = ax.legend(loc='upper right', shadow=True)
for label in legend.get_texts():
    label.set_fontsize('x-small')

fig.autofmt_xdate()
plt.show()
fig.savefig('b.pdf', dpi=300)
plt.close(fig)


sys.exit(1)
index = -1
x_dict = []
y_dict = []

pos = 0
for item in x:
    if item not in x_dict:
        x_dict.append(item)
        y_dict.append(y[index+1])
        pos += 1
    else:
        y_dict[index] += y[pos]
        pos += 1
#print len(x_dict), len(y_dict)


fig, ax = plt.subplots()
ax.plot(x_dict, y_dict)
plt.xlabel('Time (10 Mins)')
plt.ylabel('Aggregate Number of Requests')
ax.autoscale_view()
fig.autofmt_xdate()
fig.savefig('/home/susmit/Code/netsec_git/papers/16-susmit-icn/qos/pics/aggregate_requests.pdf', dpi=300)




#  plt.show()
#except:
#  pass
