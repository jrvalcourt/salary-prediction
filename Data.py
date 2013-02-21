import csv
import pandas
import pprint

'''
Import the training data and parse it
into a pandas data frame
'''

def get_data(fname='data/Train.csv'):
    d = {}
    with open(fname) as fin:
        header = fin.readline().strip().split(',')
        reader = csv.reader(fin)
        for row in reader:
            d[row[0]] = {feat : val for feat, val in enumerate(row[1:])}
        data = pandas.DataFrame.from_dict(d, orient='index')
        data.columns = header
        return data

if __name__ == '__main__':
    data = get_data('data/Train.csv')
    print data 
