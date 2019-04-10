###return IP list from a CSV file
import sys 
import csv
import operator
from collections import Counter
import re

log = sys.argv[1]
asn_list = set()

with open(log, 'r') as f:

    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        asn = row[5]
        print(asn)
        asn_list.add(asn)

with open(sys.argv[2], 'w') as w:
    w.write('\n'.join(asn_list))

