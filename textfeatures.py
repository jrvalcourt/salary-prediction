import datagetter, nltk, time, sys, os.path, operator, pandas, collections, math
import cPickle as pickle
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

#def count_word_occurences_in_row(row, words, start_time=None):
#    if not int(row.name) % 1000: 
#    print 'Finished {0} in {1} s'.format(row.name, time.time() - start_time)
#    word_counts = []
#    for word in words:
#        count, length = 0, 0
#        for sentence in nltk.sent_tokenize(row['FullDescription']):
#            curr_words = nltk.word_tokenize(sentence)
#            count += curr_words.count(word)
#            length += len(sentence)
#        word_counts.append(count / float(length))
#    print word_counts[:10], len(word_counts), words[:10], len(words)
#    return pandas.Series(word_counts, index=words)

# yield chunks of the data in tokenized form
#def chunk_generator(n, name, chunksize=50000):
#    num_of_chunks = int(math.ceil(len(data) / float(chunksize)))
#    for chunknum in range(num_of_chunks):
#        chunkfile = 'temp/{0}-{1}-{2}.p'.format(name, chunknum, num_of_chunks)
#        if not os.path.exists(chunkfile):
#            print 'Tokenizing chunk {0} of {1}'.format(chunknum + 1, num_of_chunks)
#            chunk = [[word for sentence in nltk.sent_tokenize(text) 
#                    for word in nltk.word_tokenize(sentence)] 
#                    for text in n[chunknum * chunksize:(chunknum + 1) * chunksize]]
#            pickle.dump(chunk, open(chunkfile, 'wb'))
#            yield chunknum, num_of_chunks, chunk
#        else:
#            print 'Reading precalculated chunk {0} of {1}'.format(chunknum + 1, num_of_chunks)
#            yield chunknum, num_of_chunks, pickle.load(open(chunkfile, 'rb'))

def how_many_chunks(n, chunksize=50000):
    return int(math.ceil(n / float(chunksize)))

def get_tokenized_chunk(n, name, chunknum, chunksize=50000):
    num_of_chunks = how_many_chunks(len(data), chunksize)
    chunkfile = 'temp/{0}-{1}-{2}.p'.format(name, chunknum, num_of_chunks)
    if not os.path.exists(chunkfile):
        print 'Tokenizing chunk {0} of {1}'.format(chunknum + 1, num_of_chunks)
        chunk = [[word for sentence in nltk.sent_tokenize(text)
                for word in nltk.word_tokenize(sentence)]
                for text in n[chunknum * chunksize:(chunknum + 1) * chunksize]]
        pickle.dump(chunk, open(chunkfile, 'wb'))
        return chunk
    else:
        print 'Reading precalculated chunk {0} of {1}'.format(chunknum + 1, num_of_chunks)
        return pickle.load(open(chunkfile, 'rb'))

def collate(name):
    print 'Collating answer "{0}"...'.format(name)
    tempfiles = os.listdir('temp')
    for filename in tempfiles:
        if filename.startswith(name + '-'): 
            break
    num_of_chunks = int(filename.split('-')[-1])
    answer = []
    for ii in range(num_of_chunks):
        print 'Adding answer chunk {0} of {1}'.format(ii + 1, num_of_chunks)
        answer.extend(pickle.load(open('{0}-{1}-{2}.p'.format(name, ii, num_of_chunks),'rb')))
    return answer

def get_word_count_feats(data, words_to_count, answer_name):
#    start = time.time()
#    feats = data.apply(lambda x: count_word_occurences_in_row(x, words_to_count, start), axis=1)
#    pickle.dump(feats, open(savefile, 'wb'))

    final_name = 'temp/{0}_full.p'.format(answer_name)

    if os.path.exists(final_name):
        return pickle.load(open(final_name, 'rb'))

    start = time.time()
    name = 'pretokenized'
    total = how_many_chunks(len(data['FullDescription']), chunksize=50000)
    for ii in range(total):
        answer_file = 'temp/{0}-{1}-{2}.p'.format(answer_name, ii, total)
        if not os.path.exists(answer_file):
            print 'Started counting words in chunk {0} of {1} at {2} s'.format(ii + 1, total, time.time() - start)
            chunk = get_tokenized_chunk(data['FullDescription'], name, ii, chunksize=50000)
            answer = [[text.count(word) for word in words_to_count] 
                    for text in chunk]
            pickle.dump(answer, open(answer_file, 'wb'))
        else:
            print 'Chunk {0} of {1} is already computed at {2} s'.format(ii + 1, total, time.time() - start)
    print 'Done at {0} s'.format(time.time() - start)
    pickle.dump(answer, open(final_name, 'wb'))

    return collate(answer_name)

#    for curr_word in words_to_count:
#        if os.path.exists('temp/word_counts/{0}.p'.format(curr_word)):
#
#        print 'Counting for {0}'.format(curr_word)
#        per_desc_counts = []
#        for ii, text in enumerate(data['FullDescription']):
#            if not ii % 1000: print ii
#            count = 0
#            for sentence in nltk.sent_tokenize(text):
#                count += nltk.word_tokenize(sentence).count(curr_word)
#            per_desc_counts.append(count)
#        data = data.append(per_desc_counts, ignore_index=True)
#        print 'Finished counting the frequencies of {0} words in {1} s'.format(ii, time.time() - start)
#    return data

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
#    print lengths

    data = datagetter.get_data()
    feats = get_word_count_feats(data, [word for word, val in sorted_counts[:500]], 'top500')

    
    print feats
    
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
