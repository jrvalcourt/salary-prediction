import datagetter, nltk, time, sys, os.path, operator, pandas
import cPickle as pickle
from collections import defaultdict
import matplotlib.pyplot as plt

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

def count_words(text):
    words = nltk.tokenize.word_tokenize(text)
    counts = dict_maker()
    for word in words:
        counts[word] += 1
    return counts

def read_counts(fin):
    try:
        counts = pickle.load(open(fin, 'rb'))
        return counts
    except IOError:
        return None

def get_all_counts(counts_file):
    counts = None
    if not os.path.exists(counts_file):
        print 'Counting all words in all descriptions.'
        counts = count_all_words('data/Train.csv', counts_file)
    else:
        print 'Reading counts file.'
        counts = read_counts(counts_file)
    return counts

def add_feats(data, sorted_counts):
    for text in data['FullDescription']:
        desc_counts = count_words(text)
        total_words = float(len(nltk.tokenize.word_tokenize(text)))
        desc_freq = {}
        for word in desc_counts:
            desc_freq[word] = desc_counts[word] / total_words
    pandas.Series([pair[0] for pair in sorted_counts[:500]], index=data.index)

if __name__ == '__main__':
    counts = get_all_counts('total_word_counts.p')
    if not counts:
        sys.stderr.write('Something went wrong when reading the file.')
    sorted_counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
#    for ii, pair in enumerate(sorted_counts[:100]):
#        print '{0}: {1} - {2}'.format(ii, pair[0], pair[1])
    data = datagetter.get_data()
    add_feats(data, sorted_counts)

    print data

    plt.bar([ii for ii in range(100)], [val[1] for val in sorted_counts[:100]])
    plt.show()


