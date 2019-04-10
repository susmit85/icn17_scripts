import pyasn
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import operator
import sys

asndb = pyasn.pyasn('/raid/LLNL_ACCESS_LOG/scripts/ipasn_20150224.dat')

def plot_route_from_ips(ip_list):
    asn_list = [str(asndb.lookup(ip)[0]) for ip in ip_list]
    print("->".join(asn_list))


def ip_dict_from_file(filename):
    ip_dict = {}
    with open(filename, 'r') as f:
        for line in f:
            comps = line.split("\t")
            user, ip = comps[1],comps[5]
            try:
                ip_dict[ip].add(user)
            except KeyError:
                ip_dict[ip] = {user} #this is a set
    return(ip_dict)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="filename", required=True)
    args = parser.parse_args()

    filename = args.filename
    ip_dict = ip_dict_from_file(filename)
#    print(ip_dict)
    asn_dict = {}
    asn = ""
    for ip, users in ip_dict.items():
        user_list = [user for user in users]
        try:
            asn = asndb.lookup(ip)[0]
            asn_dict[asn].extend(user_list)
        except KeyError:
            asn_dict[asn] = user_list
        except ValueError:
            print("Value error for ", asn, ip)
            pass

    print(len(asn_dict))

    
a = {}    
for key, value in asn_dict.items():
    a[key] = len(value)
print(sorted(a.items(), key=operator.itemgetter(1)))
x = [i for i in range(len(asn_dict))]
y = [len(j) for j in asn_dict.values()]

hist_x = [x*10 for x in range(70)]
hist_y, bin_edges = np.histogram(y, hist_x)
cum_hist_y = np.cumsum(hist_y)
cdf = [0] + [i/sum(hist_y) for i in cum_hist_y]


print(hist_x, cum_hist_y, cdf)

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.grid()
ax1.set_ylim(0,1)
print(len(hist_x), len(cdf))
ax1.plot(hist_x, cdf, label="Users/ASN")
ax1.set_xlabel("Number of ASNs")
ax1.set_ylabel("CDF of users")
plt.legend(loc='upper right')

#ax2 = fig.add_subplot(212)
#ax2.plot(x,y)

plt.savefig('users_per_asn_cdf.png', dpi=300)


