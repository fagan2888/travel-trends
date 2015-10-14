import os
import csv

def MakePath(folder, file):
    origin = os.getcwd().split('\\')
    source = origin[0:len(origin)-1]
    source.append(folder)
    source.append(file)
    path = '\\'.join(source)
    return path

path = MakePath('fixtures', 'CountryList.csv')
with open(path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for line in reader:
        print(line[2])
