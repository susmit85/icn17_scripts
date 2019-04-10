import pygeoip as geo
from collections import OrderedDict

gi = geo.GeoIP('GeoLiteCity.dat')
hit_dict = {}
#what's the output format? 
with open ('request_ip_addresses.txt', 'r') as source:
  #how big can the input be? speed vs space
  #clarify delimiter
  lines = source.read().split('\n')
  for item in lines:
      #get the record
#      print(item)
      try:
        hit_dict[item] += 1
      except KeyError:
        hit_dict[item] = 1


sorted_hit_dict = sorted(hit_dict.items(), key=lambda x:x[1])
item_count = 0
for item in reversed(sorted_hit_dict):
    requestRecord = gi.record_by_addr(item[0])
    lat = requestRecord['latitude']
    lon = requestRecord['longitude']
    city = requestRecord['city']
    print("%s,%s,%s,%s,%s" %(item[0],item[1],lat,lon,city))
    item_count += 1
    if item_count == 100:
        break
  
      
