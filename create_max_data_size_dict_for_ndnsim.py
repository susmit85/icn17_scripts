import csv
import sys


file_size_dict = {}
with open(sys.argv[1], 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        filename = row[3]
        filesize = int(row[-2])
        try:
            if file_size_dict[filename] <  filesize: 
                file_size_dict[filename] =  filesize
        except KeyError:
             file_size_dict[filename] =  filesize if filesize != -1 else 1
    
total = 0    
with open(sys.argv[1], 'r') as csvfile:
    with open('../LLNL_ACCESS_LOG_SANITIZED_FILESIZES.csv', 'w') as w:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            filename = row[3]
#        print("old", row)
            row[-2] = str(file_size_dict[filename])
            #total += row[-2]
            w.write("\t".join(row))

#    print(total)        

