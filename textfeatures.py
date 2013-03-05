import datagetter, nltk, time, sys, os.path, operator, pandas
import cPickle as pickle
from collections import defaultdict
import matplotlib.pyplot as plt

DATA_FILE = 'data/Train.csv'

def dict_maker():
    return defaultdict(int)


#################################################################################
# Word count functions
#################################################################################
'''
def count_all_words(file_in, file_out):
    counts = defaultdict(int)
    lengths = defaultdict(int)
    data = datagetter.get_data(file_in)
    start = time.time()
    for ii, text in enumerate(data['FullDescription']):
        sentences = nltk.tokenize.sent_tokenize(text) 
        for sentence in sentences:
            words = nltk.tokenize.word_tokenize(sentence)
            sentence_length = 0
            for word in words:
                counts[word] += 1
                sentence_length += 1
            lengths[ii] = sentence_length 
        if not ii % 1000: 
            print 'Finished {:d} ads in {:.2f} seconds'.format(ii, time.time() - start)
    pickle.dump(counts, open(file_out, "wb"))
    return counts

# Delete function?
def count_words(text):
    words = nltk.tokenize.word_tokenize(text) #NLTK documentation cautions to only use this method on single sentences
    counts = dict_maker()
    for word in words:
        counts[word] += 1
    return counts
'''

# Returns word counts and sentence lengths in all ads
def get_all_counts_and_lengths(counts_file, lengths_file):
    #counts = None
    if not os.path.exists(counts_file) or not os.path.exists(lengths_file):
        print 'Counting all words in all descriptions.'
        #counts = count_all_words(DATA_FILE, counts_file)

        counts = defaultdict(int)
        lengths = defaultdict(int)
        data = datagetter.get_data(DATA_FILE)
        start = time.time()
        for ii, text in enumerate(data['FullDescription']):
            sentences = nltk.tokenize.sent_tokenize(text)
            total_words = 0 # Keeps track of total words in each ad
            for sentence in sentences:
                words = nltk.tokenize.word_tokenize(sentence)
                total_words += len(words)
                for word in words:
                    counts[word] += 1 # Track number of instances of a word
            # Track number of sentences and total number of words per ad
            lengths[ii] = len(sentences), total_words
            if not ii % 1000: 
                print 'Finished {:d} ads in {:.2f} seconds'.format(ii, time.time() - start)
        pickle.dump(counts, open(counts_file, "wb"))
        pickle.dump(lengths, open(lengths_file, "wb"))
    else:
        print 'Reading counts and lengths file.'
        counts = datagetter.read_file(counts_file)
        lengths = datagetter.read_file(lengths_file)
    return counts, lengths 

def add_feats(data, sorted_counts):
    most_freq_words = [word for word, val in sorted_counts[:500]]
    all_freqs = {}
    start = time.time()
    for ii, text in enumerate(data['FullDescription']):
        desc_counts = count_words(text)
        total_words = float(len(nltk.tokenize.word_tokenize(text)))
        desc_freq = dict_maker()
        for word in desc_counts:
            desc_freq[word] = desc_counts[word] / total_words
        all_freqs[ii] = desc_freq
        if not ii % 1000:
            print 'Counted frequencies in {0} ads in {1} s'.format(ii, time.time() - start)
    for word, val in sorted_counts[:500]:
        data[word] = pandas.Series([all_freqs[d][word] for d in all_freqs], index=data.index)

#################################################################################
# Mean sentence length functions
#################################################################################

# Returns mean sentence length for each description
'''
def get_mean_sentence_lengths(sentence_length_file):
    if not os.path.exists(sentence_length_file):
        print 'Counting sentence length in all descriptions'
        lengths = defaultdict(int)
        data = datagetter.get_data(DATA_FILE)
        start = time.time()

        # Alt method requires download of NLTK Punkt training models
        # tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        # print '\n-----\n'.join(tokenizer.tokenize(text)) 

        for ii, text in enumerate(data['FullDescription']):
            sentences = nltk.tokenize.sent_tokenize(text)  #NLTK documentation cautions to only use this method on single sentences
            for sentence in sentences:
            if not ii % 1000: 
                print 'Finished {:d} ads in {:.2f} seconds'.format(ii, time.time() - start)
        pickle.dump(lengths, open(sentence_length_file, "wb"))
    else:
        lengths = datagetter.read_file(sentence_length_file)
        print 'Reading sentence length file'
    return lengths
'''


#################################################################################
# Script
#################################################################################
if __name__ == '__main__':
    counts, lengths = get_all_counts_and_lengths('temp/total_word_counts.p', 'temp/sentence_lengths.p')
    if not counts:
        sys.stderr.write('Something went wrong reading the counts file.')
    sorted_counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
    #for ii, pair in enumerate(sorted_counts[:100]):
    #    print '{0}: {1} - {2}'.format(ii, pair[0], pair[1])
    
    if not lengths:
         sys.stderr.write('Something went wrong reading the lengths file.')
    print lengths
    
    ''' 
    data = datagetter.get_data()
    add_feats(data, sorted_counts)

    pickle.dump(data, open('annotated_data.p', 'wb'))

    print data

<<<<<<< HEAD
#    plt.bar([ii for ii in range(100)], [val[1] for val in sorted_counts[:100]])
#    plt.show()
=======
    plt.bar([ii for ii in range(100)], [val[1] for val in sorted_counts[:100]])
    plt.show()
    '''

    


>>>>>>> 2a35a2814e6021c6027b2af1aab9bca489185797


