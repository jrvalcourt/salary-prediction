import csv
import pandas
import pprint

'''
Import the training data and parse it
into a pandas data frame
'''

def parse(fname):
    d = {}
    with open(fname) as fin:
        reader = csv.reader(fin)
        for row in reader:
            d[row[0]] = {feat : val for feat, val in enumerate(row[1:])}
        data = pandas.DataFrame.from_dict(d, orient='index')
        return data

if __name__ == '__main__':
    data = parse('data/Train.csv')
    print data 
