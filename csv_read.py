import csv

with open('categorias.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print row['cod']
