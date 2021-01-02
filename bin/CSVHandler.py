import csv
import shutil
from tempfile import NamedTemporaryFile
import time
import os
import collections

def updateCSVFile(file_name, members):
    if members == None:
        return

    if not os.path.exists(file_name):
        open(file_name, 'a').close()

    d = parseCSVFile(file_name)

    for member in members:
        if str(member) in d:
            d[str(member)] += 1
        else:
            d[str(member)] = 1

    sorted_list = sorted(d.items(), key=lambda kv: kv[1])
    sorted_list.reverse()

    with open(file_name, 'w+') as f: 
        for (key,val) in sorted_list:
            csv_entry = "{},{}\n"
            f.write(csv_entry.format(key, val))

            

#input: csvfile name as string
#output: dictionary of [name: time_spent]
def parseCSVFile(file_name):
    with open(file_name, "r") as f:
        rows = f.readlines()
        d = {}
        for row in rows:
            row = row.split(',')
            if len(row) >= 2:
                d[row[0]] = int(row[1].strip())

        return d
    return {}
            
    

