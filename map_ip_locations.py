import pygeoip as geo
import csv
import sys

class ip_object:
    def __init__(self, val):
        self._ip_val = val
        self._lat = 0
        self._lon = 0
        self._city = ""
        self._error = 0
    

ip_obj_list = {}
gi = geo.GeoIP('/raid/LLNL_ACCESS_LOG/GeoLiteCity.dat')
#what's the output format? 
with open('heavy_hitter_locations.csv', 'w') as dest:
    with open (sys.argv[1], 'r') as source:
      reader = csv.reader(source, delimiter='\t')
      for row in reader:
          error = False
          time,ip,flag,req_size,xfer_size = int(row[8]),row[5], row[10], int(row[14]), int(row[15])
          if flag == 'f' or req_size <= 0 or xfer_size < req_size:
              error = True

          if ip not in ip_obj_list:
              ip_obj_list[ip] = ip_object(ip)
              ip_obj = ip_obj_list[ip]
              try:
                  requestRecord = gi.record_by_addr(ip)
                  lat = requestRecord['latitude']
                  lon = requestRecord['longitude']
                  city = requestRecord['city']
                  ip_obj._lat = lat
                  ip_obj._lon = lon
                  ip_obj._city = city
                  if error:
                    ip_obj._error += 1
              except:
                  print ("Error Processing %s" %(ip))
          else:
              if error:
                  ip_obj_list[ip]._error += 1




for key,val in ip_obj_list.items():
    print(",".join([str(key), str(val._lon), str(val._lat), str(val._city), str(val._error)]))

#                  dest.write("%s,%s,%s,%s\n" %(ip,lat,lon,city))
