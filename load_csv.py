import csv

with open("C:\\Users\\LENOVO\\Desktop\\data.csv", 'r') as fileinput:
    data = list(csv.reader(fileinput))
    print(len(data))
    print(len(data[0]))
    print(data[0])
    # for row in csv.reader(fileinput):
    #     print(row)