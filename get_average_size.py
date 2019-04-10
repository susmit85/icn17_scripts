
import sys
import traceback
ip_dict = {}
ip_count_dict = {}
ips = ["103.37.201.21","103.37.201.31","130.206.30.86","136.172.30.61","140.172.240.95","146.83.8.135","149.171.147.29","157.82.156.76","159.226.234.18","222.195.137.73"]
with open('/raid/LLNL_ACCESS_LOG/LLNL_access_logging_extract.csv', 'r') as f:
    for line in f:
       if any(ip in line for ip in ips):
           size = int(line.split()[14])
           ip = line.split()[5]
#           print(ip, size)
           if size != -1:
               try:
                 ip_dict[ip] += size
                 ip_count_dict[ip] += 1
               except KeyError:
                 ip_dict[ip] = size
                 ip_count_dict[ip] = 1

for ip in ips:
    try:
        print("IP =" + ip + "Size Avg = " + str((ip_dict[ip]/ip_count_dict[ip])))
    except:
        traceback.print_exc(file=sys.stdout)
        pass
