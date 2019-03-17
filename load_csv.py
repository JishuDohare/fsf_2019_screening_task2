import csv

with open("C:\\Users\\LENOVO\\Desktop\\data.csv", 'r') as fileinput:
    for row in csv.reader(fileinput):
        print(row)