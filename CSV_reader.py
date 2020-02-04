import csv


def CSV_reader(doc):
    with open(doc, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append(row)
        return data
