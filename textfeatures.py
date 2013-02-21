import datagetter, nltk, time, sys, os.path, operator
import cPickle as pickle
from collections import defaultdict

def dict_maker():
    return defaultdict(int)

def count_all_words(file_in, file_out):
    counts = defaultdict(int)
    data = datagetter.get_data(file_in)
    start = time.time()
    for ii, text in enumerate(data['FullDescription']):
        words = nltk.tokenize.word_tokenize(text)
        for word in words:
            counts[word] += 1
        if not ii % 1000:
            print 'Finished {:d} ads in {:.2f} seconds'.format(ii, time.time() - start)
    pickle.dump(counts, open(file_out, "wb"))
    return counts

def read_counts(fin):
    try:
        counts = pickle.load(open(fin, 'rb'))
        return counts
    except IOError:
        return None

#        index_counts[index][word] += 1
#    index = data.index[ii]
#index_counts = defaultdict(dict_maker)

if __name__ == '__main__':
    counts_file = 'total_word_counts.p'
    if not os.path.exists(counts_file):
        print 'Counting all words in all descriptions.'
        counts = count_all_words('data/Train.csv', counts_file)
    else:
        print 'Reading counts file.'
        counts = read_counts(counts_file)
    if not counts:
        sys.stderr.write('Something went wrong when reading the file.')
    sorted_counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
    for ii, pair in enumerate(sorted_counts[:100]):
        print '{0}: {1} - {2}'.format(ii, pair[0], pair[1])


