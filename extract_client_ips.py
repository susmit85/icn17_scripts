###return IP list from a CSV file
import sys 
import csv
import operator
from collections import Counter
import re

log = sys.argv[1]
ip_list = set()
ip_pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

with open(log, 'r') as f:
    reader = f.read()
    for row in reader.split('\n'):
        ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', row )
        if len(ip) == 0:
            print(row)
        
        try:
            ip_list.add(ip[0])
        except:
            pass
            print(row)

print(len(ip_list))
with open(sys.argv[2], 'w') as w:
    w.write('\n'.join(ip_list))

