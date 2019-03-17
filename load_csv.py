import csv

fileinput = open("C:\\Users\\LENOVO\\Desktop\\data.csv", 'r')
data = list(csv.reader(fileinput))
print(len(data))
print(len(data[0]))
print(data[0])
# for row in csv.reader(fileinput):
#     print(row)