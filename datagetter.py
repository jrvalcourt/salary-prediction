import csv, pandas, sys, time
import cPickle as pickle

'''
Import the training data and parse it
into a pandas data frame
'''

def get_data(fname='data/Train.csv'):
    return pandas.read_csv(fname)
    #d = {}
    #with open(fname) as fin:
    #    a = time.time()
    #    print 'Reading data...',
    #    sys.stdout.flush()
    #    header = fin.readline().strip().split(',')[1:]
    #    reader = csv.reader(fin)
    #    for ii, row in enumerate(reader):
    #        d[row[0]] = {header[feat] : val for feat, val in enumerate(row[1:])}
    #    print 'done.' 
    #    print 'Constructing data frame...',
    #    sys.stdout.flush()
    #    data = pandas.DataFrame.from_dict(d, orient='index')
    #    print 'done.'
    #    print 'Fetched data in {0} seconds.'.format(time.time() - a)
    #    return data

if __name__ == '__main__':
    data = get_data('data/Train.csv')
    print data 

# Convenience function for loading pickle files
def read_file(fin):
    try:
        contents = pickle.load(open(fin, 'rb'))
        return contents
    except IOError:
        return None

