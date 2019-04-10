import pyasn
import argparse
import csv

asndb = pyasn.pyasn('/raid/LLNL_ACCESS_LOG/scripts/ipasn_20150224.dat')

def asn_lookup(ip):
    asn = asndb.lookup(ip)[0]
    return(asn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="filename", required=True)
    args = parser.parse_args()

    filename = args.filename

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter ='\t')
        for row in reader:
            try:
                ip = row[5]
                xfer_size = int(row[-1])
                file_size = int(row[-2])

                if xfer_size > 0 and file_size > 0:
                    asn = asndb.lookup(ip)[0]
                    row[5] = str(asn)
                    print("\t".join(row))
            except:
                pass
