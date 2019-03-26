import csv

fileinput = open("C:\\Users\\LENOVO\\Desktop\\data4.csv", 'r')
data = list(csv.reader(fileinput))
print(len(data))
print(len(data[0]))
print(data[0])
data[0][0] = 232323
data[0][1] = 323232
with open("C:\\Users\\LENOVO\\Desktop\\data4.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
