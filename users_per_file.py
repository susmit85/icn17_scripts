import pyasn
import argparse
import maplotlib.pyplot as plt
import numpy as np

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
 #       print(asn)
        try:
            asn = asndb.lookup(ip)[0]
            asn_dict[asn].extend(user_list)
        except KeyError:
            asn_dict[asn] = user_list
        except ValueError:
            print("Value error for ", asn, ip)
            pass

    print(len(asn_dict))


x = [i for i in range(len(asn_dict))]
y = [len(j) for j in asn_dict.values()]

fig = plt.figure(111)


