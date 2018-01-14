# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:45:59 2017

@author: Rasmus
"""

# module imports
import nltk
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt


# constants
TOKEN_REGEXP = r'''(?x)    # set flag to allow verbose regexps
  (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
| Mr\.|Mrs\.|Jr\.|Ms\.
| Jan\.|Feb\.|Mar\.|Apr\.|Jun\.|Jul\.|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.
| Ill\.|Wis\.|Cali\.|Miss\.|Wash\.|Mich\.|Fla\.|Mass\.
| Inc\.|Co\.|Ltd\.|Corp\.
| Doc\.|Conn\.|Colo\.|Dr\.
| Messrs\.
| St\.
| Rep\.
#| (?:Mc')*\W\w*([-/]\W\w+)*
| 's | 'll
| n't|\w+(?=n't)
| 're|\w+(?='re)
| \w+(?:-\w+)+      # words with internal hyphens
| \d+(?:\.\d+)      # numbers with decimals
| \d+(?:\,\d+)+     # Thousands and millions
| \d+(?:\/\d+)+     # fractions
| [A-Z]+[a-z]+      # words starting with capital letter
| \w+               # whatever lower-case words are left
| --                # long dash
| [][.,;"'?():-_`\%$&{}]  # these are separate tokens; includes ], [
'''


def get_corpus_text(nr_files=199):
    """Returns the raw corpus as a long string.
    'nr_files' says how much of the corpus is returned;
    default is 199, which is the whole corpus.
    """
    fileids = nltk.corpus.treebank_raw.fileids()[:nr_files]
    corpus_text = nltk.corpus.treebank_raw.raw(fileids)
    # Get rid of the ".START" text in the beginning of each file:
    corpus_text = corpus_text.replace(".START", "")
    return corpus_text

def fix_treebank_tokens(tokens):
    """Replace tokens so that they are similar to the raw corpus text."""
    return [token.replace("''", '"').replace("``", '"').replace(r"\/", "/")
            for token in tokens]

def get_gold_tokens(nr_files=199):
    """Returns the gold corpus as a list of strings.
    'nr_files' says how much of the corpus is returned;
    default is 199, which is the whole corpus.
    """
    fileids = nltk.corpus.treebank_chunk.fileids()[:nr_files]
    gold_tokens = nltk.corpus.treebank_chunk.words(fileids)
    return fix_treebank_tokens(gold_tokens)


def tokenize_corpus(text):
    """Don't forget the docstring!"""
    return nltk.regexp_tokenize(text, TOKEN_REGEXP)

def evaluate_tokenization(test_tokens, gold_tokens):
    """Finds the chunks where test_tokens differs from gold_tokens.
    Prints the errors and calculates similarity measures.
    """
    import difflib
    matcher = difflib.SequenceMatcher()
    matcher.set_seqs(test_tokens, gold_tokens)
    error_chunks = true_positives = false_positives = false_negatives = 0
    print(" Token%30s  |  %-30sToken" % ("Error", "Correct"))
    print("-" * 38 + "+" + "-" * 38)
    for difftype, test_from, test_to, gold_from, gold_to in matcher.get_opcodes():
        if difftype == "equal":
            true_positives += test_to - test_from
        else:
            false_positives += test_to - test_from
            false_negatives += gold_to - gold_from
            error_chunks += 1
            test_chunk = " ".join(test_tokens[test_from:test_to])
            gold_chunk = " ".join(gold_tokens[gold_from:gold_to])
            print("%6d%30s  |  %-30s%d" % (test_from, test_chunk, gold_chunk, gold_from))
    precision = 1.0 * true_positives / (true_positives + false_positives)
    recall = 1.0 * true_positives / (true_positives + false_negatives)
    fscore = 2.0 * precision * recall / (precision + recall)
    print()
    print("Test size: %5d tokens" % len(test_tokens))
    print("Gold size: %5d tokens" % len(gold_tokens))
    print("Nr errors: %5d chunks" % error_chunks)
    print("Precision: %5.2f %%" % (100 * precision))
    print("Recall:    %5.2f %%" % (100 * recall))
    print("F-score:   %5.2f %%" % (100 * fscore))
    print()

def find_nbr_word_tokens(corpus):
    """ Returns the number of word tokens in the corpus. """
    tokens = tokenize_corpus(corpus)
    return len(tokens)
    
def find_nbr_word_types(corpus):
    """ Returns the number of word types in the corpus. """
    tokens = tokenize_corpus(corpus)
    return len(set(tokens))

def find_average_token_length(corpus):
    """ Returns the average token length in the corpus. """
    tokens = tokenize_corpus(corpus)
    return np.mean([len(x) for x in tokens])
    
def find_longest_words(corpus):
    """ Finds the longest words in the corpus. Returns a tuple, the first 
    element being a list of the longest words, and the second element being
    the maximum word length. """
    tokens = tokenize_corpus(corpus)
    word_types = set(tokens)
    longest_words = []
    max_length = 0
    
    for word in word_types:
        word_length  = len(word)
        if word_length < max_length:
            pass # do nothing
        elif word_length == max_length:
            longest_words.append(word)
        else: # meaning new max lenght found
            max_length = word_length
            longest_words = [word] # Reset the list
    return (longest_words, max_length)

def find_frequencies(corpus): 
    """ Returns a dictionary with the counts for each word type. """
    tokens = tokenize_corpus(corpus) 
    frequencies = {}
    for token in tokens:
        try:
            frequencies[token] += 1
        except KeyError:
            frequencies[token] = 1
    return frequencies

def find_hapax_words(corpus):
    """ Returns a list of all the hapax word types in the corpus. """
    frequencies = find_frequencies(corpus)
    hapax_words = []
    for word, freq in frequencies.items():
        if freq == 1:
            hapax_words.append(word)
    return hapax_words
     
def find_nbr_hapax_tokens(corpus):
    """ Returns the number of hapax word tokens in the corpus. """
    frequencies = find_frequencies(corpus)
    nbr_hapax_tokens = 0
    for word, freq in frequencies.items():
        if freq == 1:
            nbr_hapax_tokens += 1
    return nbr_hapax_tokens
            
def find_hapax_fraction(corpus):
    """ Returns the fraction of tokens in the corpus that are hapax words. """
    return find_nbr_hapax_tokens(corpus)/find_nbr_word_tokens(corpus)

def find_most_frequent_words(corpus, N):
    """ Returns a list of tuples of the word type and its counts of the N most 
    frequent word types in the corpus. """
    freqs = find_frequencies(corpus)
    sorted_freqs = sorted(freqs.items(), key=itemgetter(1))
    sorted_freqs.reverse()
    return [x[0] for x in sorted_freqs[0:N]]

def find_most_frequent_words_fraction(corpus, N):
    """ Returns the fraction of tokens in the corpus that are of the N most 
    common word types. """
    freqs = find_frequencies(corpus)
    sorted_freqs = sorted(freqs.items(), key=itemgetter(1))
    sorted_freqs.reverse()
    return sum([x[1] for x in sorted_freqs[0:N]])/find_nbr_word_tokens(corpus)


def find_nbr_bigram_types(corpus):
    """ Returns the number of bigrams types in the corpus, in absolute numbers
    and as a fraction of all the bigrams. """
    tokens = tokenize_corpus(corpus)
    bigrams = nltk.bigrams(tokens)
    freqs = nltk.FreqDist(bigrams)
    nbr_types = freqs.B()
    nbr_tokens = freqs.N()
    fraction = nbr_types/nbr_tokens
    return nbr_types, fraction


def find_nbr_unique_bigrams(corpus):
    """ Returns the number of unique bigrams in the corpus, in absolute numbers
    and as a fraction of all the bigrams. """
    tokens = tokenize_corpus(corpus)
    bigrams = nltk.bigrams(tokens)
    freqs = nltk.FreqDist(bigrams)
    nbr_unique = 0
    tots = 0
    for sample in freqs:
        tots += 1
        if freqs[sample] == 1:
            nbr_unique += 1
    fraction = nbr_unique/tots
    return nbr_unique, fraction

def find_nbr_trigram_types(corpus):
    """ Returns the number of trigrams types in the corpus, in absolute numbers
    and as a fraction of all the trigrams. """
    tokens = tokenize_corpus(corpus)
    trigrams = nltk.trigrams(tokens)
    freqs = nltk.FreqDist(trigrams)
    nbr_types = freqs.B()
    nbr_tokens = freqs.N()
    fraction = nbr_types/nbr_tokens
    return nbr_types, fraction

def find_nbr_unique_trigrams(corpus):
    """ Returns the number of unique trigrams in the corpus, in absolute numbers
    and as a fraction of all the bigrams. """
    tokens = tokenize_corpus(corpus)
    trigrams = nltk.trigrams(tokens)
    freqs = nltk.FreqDist(trigrams)
    nbr_unique = 0
    tots = 0
    for sample in freqs:
        tots += 1
        if freqs[sample] == 1:
            nbr_unique += 1
    fraction = nbr_unique/tots
    return nbr_unique, fraction


def sub_corpus_hapax_fractions(corpus, nbr_slices):
    """ Divides the corpus in equal-sized slices and returns the fraction of 
    tokens that are hapax words in each slice. """
    slice_size = int(len(corpus)/nbr_slices)
    hapax_fractions = np.zeros(nbr_slices)
    for i in range(nbr_slices):
        i_corpus = corpus[i*slice_size: (i+1)*slice_size]
        hapax_fractions[i] = find_hapax_fraction(i_corpus)
    return hapax_fractions

def corpus_size_vs_hapax_fraction(corpus, nbr_slices):
    """ Divides the corpus in cumulative slices and calculates the fraction of 
    tokens that are hapax words in each slice. Returns two lists, the first 
    being the hapax fractions and the second being the number of tokens in
    each slice.  """
    slice_size = int(len(corpus)/nbr_slices)
    hapax_fractions = np.zeros(nbr_slices)
    corpus_sizes = np.zeros(nbr_slices)
    for i in range(nbr_slices):
        i_corpus = corpus[0: (i+1)*slice_size]
        hapax_fractions[i] = find_hapax_fraction(i_corpus)
        corpus_sizes[i] = find_nbr_word_tokens(i_corpus)
    return hapax_fractions, corpus_sizes

def plot_supcorpus_hapax_fractions(corpus, nbr_slices):
    """ Plots the hapax fraction for non-overlapping sub-corpuses of equal 
    size. """
    hapax_fractions = sub_corpus_hapax_fractions(corpus, nbr_slices)
    plt.plot(hapax_fractions)
    plt.xlabel('Slice number')
    plt.ylabel('Fraction of hapax tokens ')
    plt.title('Hapax fraction for equal-sized sub-corpuses')
    plt.ylim([0, 1.2*max(hapax_fractions)])
    plt.savefig('sub_corpus_hapax_fraction.png', dpi = 800)

def plot_size_vs_hapax(corpus, nbr_slices):
    """ Makes a plot of the hapax fraction as a function of corpus size by 
    dividing the corpus in overlapping sub-corpuses of increasing size. """
    hapax_fractions, corpus_sizes = corpus_size_vs_hapax_fraction(corpus, nbr_slices)
    plt.plot(corpus_sizes, hapax_fractions)
    plt.xlabel('Corpus Size')
    plt.ylabel('Fraction of hapax tokens ')
    plt.title('Hapax fraction as a function of corpus size')
    plt.ylim([0, 1.2*max(hapax_fractions)])
    plt.savefig('size_vs_hapax.png', dpi = 800)


def print_corpus_statistics(corpus):
    """ Prints a number of corpus statistics to the terminal. """
    print('Number of word tokens in corpus: %d' % find_nbr_word_tokens(corpus))    
    print('Number of word types in corpus: %d' % find_nbr_word_types(corpus))    
    print('Aveage token length: %.2f' % find_average_token_length(corpus)) 
    longest_words, max_length = find_longest_words(corpus)
    print('Maximum word length: %d' % max_length)
    print('Words with maximum length: ' + ', '. join(longest_words))
    print('Number of hapax tokens: %d' % find_nbr_hapax_tokens(corpus))
    print('The hapax word types make up %.1f%% of the corpus' % \
        (100*find_hapax_fraction(corpus)))
    print('The ten most frequent words are: ' + str(find_most_frequent_words(corpus, 10)))
    print('The ten most frequent words make up %.0f%% of the corpus' % \
        (100*find_most_frequent_words_fraction(corpus, 10)))
    print('Hapax token pecentages in ten equal-sized sub-corpuses: ' + \
        '%, '.join(['%.1f' % (100*x) for x in sub_corpus_hapax_fractions(corpus, 10)]) + \
        '%')
    print('Hapax token pecentages in ten sub-corpuses of increasing size' + \
        '(from a tenth of the corpus to the whole corpus): ' + \
        '%, '.join( \
        ['%.1f' % (100*x) for x in corpus_size_vs_hapax_fraction(corpus, 10)[0]]) + \
        '%')
    nbr_types, fraction = find_nbr_bigram_types(corpus)
    print(('Number of bigram types: %d' % nbr_types) + (', that is  %.1f%% of the corpus' % (100*fraction)))
    nbr_types, fraction = find_nbr_trigram_types(corpus)
    print(('Number of trigram types: %d' % nbr_types) + (', that is  %.1f%% of the corpus' % (100*fraction)))

def main():
    nr_files = 199
    corpus = get_corpus_text(nr_files)
    
    print('Part 1, evaluating the regex')
    print('------------------------------')
    gold_tokens = get_gold_tokens(nr_files)
    tokens = tokenize_corpus(corpus)
    evaluate_tokenization(tokens, gold_tokens)
    
    print('\n \n \nPart 2, corpus statistics')
    print('------------------------------')
    print_corpus_statistics(corpus)
    
    #plot_supcorpus_hapax_fractions(corpus, 10)
    #plot_size_vs_hapax(corpus, 10) #uncomment to make and save plot

if __name__ == "__main__":
    main()
