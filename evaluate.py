import csv
with open('Test1.csv', 'rb') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=',')
    for row in dataReader:
        print ', '.join(row)
