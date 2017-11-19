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
corpus_size = (...)
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
            tmp = test_tokens[test_from:test_to]
            try:
                test_chunk = " ".join(test_tokens[test_from:test_to])
            except TypeError as e:
                print(tmp)
                raise(e)
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
    tokens = tokenize_corpus(corpus)
    return len(tokens)
    
def find_nbr_word_types(corpus):
    tokens = tokenize_corpus(corpus)
    return len(set(tokens))

def find_average_token_length(corpus):
    tokens = tokenize_corpus(corpus)
    return np.mean([len(x) for x in tokens])
    
def find_longest_words(corpus):
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
    tokens = tokenize_corpus(corpus) 
    frequencies = {}
    for token in tokens:
        try:
            frequencies[token] += 1
        except KeyError:
            frequencies[token] = 1
    return frequencies

def find_hapax_words(corpus):
    frequencies = find_frequencies(corpus)
    hapax_words = []
    for word, freq in frequencies.items():
        if freq == 1:
            hapax_words.append(word)
    return hapax_words
     
def find_nbr_hapax_tokens(corpus):
    frequencies = find_frequencies(corpus)
    nbr_hapax_tokens = 0
    for word, freq in frequencies.items():
        if freq == 1:
            nbr_hapax_tokens += 1
    return nbr_hapax_tokens
            
def find_hapax_fraction(corpus):
    return find_nbr_hapax_tokens(corpus)/find_nbr_word_tokens(corpus)

def find_most_frequent_words(corpus, N):
    freqs = find_frequencies(corpus)
    sorted_freqs = sorted(freqs.items(), key=itemgetter(1))
    sorted_freqs.reverse()
    return [x[0] for x in sorted_freqs[0:N]]

def find_most_frequent_words_fraction(corpus, N):
    freqs = find_frequencies(corpus)
    sorted_freqs = sorted(freqs.items(), key=itemgetter(1))
    sorted_freqs.reverse()
    return sum([x[1] for x in sorted_freqs[0:N]])/find_nbr_word_tokens(corpus)

def find_nbr_bigrams(corpus):
    tokens = tokenize_corpus(corpus)
    bigrams = list(nltk.bigrams(tokens))
    return len(bigrams)

def find_nbr_unique_bigrams(corpus):
    tokens = tokenize_corpus(corpus)
    bigrams = nltk.bigrams(tokens)
    freqs = nltk.FreqDist(bigrams)
    nbr_unique = 0
    for sample in freqs:
        if freqs[sample] == 1:
            nbr_unique += 1
    return nbr_unique

def find_nbr_unique_bigrams_fraction(corpus):
    return find_nbr_unique_bigrams(corpus) / find_nbr_bigrams(corpus)

def find_nbr_trigrams(corpus):
    tokens = tokenize_corpus(corpus)
    trigrams = list(nltk.trigrams(tokens))
    return len(trigrams)

def find_nbr_unique_trigrams(corpus):
    tokens = tokenize_corpus(corpus)
    trigrams = nltk.trigrams(tokens)
    freqs = nltk.FreqDist(trigrams)
    nbr_unique = 0
    for sample in freqs:
        if freqs[sample] == 1:
            nbr_unique += 1
    return nbr_unique

def find_nbr_unique_trigrams_fraction(corpus):
    return find_nbr_unique_trigrams(corpus) / find_nbr_trigrams(corpus)

def sub_corpus_hapax_fractions(corpus, nbr_slices): 
    slice_size = int(len(corpus)/nbr_slices)
    hapax_fractions = np.zeros(nbr_slices)
    for i in range(nbr_slices):
        i_corpus = corpus[i*slice_size: (i+1)*slice_size]
        hapax_fractions[i] = find_hapax_fraction(i_corpus)
    return hapax_fractions

def corpus_size_vs_hapax_fraction(corpus, nbr_slices):
    slice_size = int(len(corpus)/nbr_slices)
    hapax_fractions = np.zeros(nbr_slices)
    corpus_sizes = np.zeros(nbr_slices)
    for i in range(nbr_slices):
        i_corpus = corpus[0: (i+1)*slice_size]
        hapax_fractions[i] = find_hapax_fraction(i_corpus)
        corpus_sizes[i] = find_nbr_word_tokens(i_corpus)
    return hapax_fractions, corpus_sizes

def make_hapax_plot(corpus, nbr_slices):
    hapax_fractions, corpus_sizes = corpus_size_vs_hapax_fraction(corpus, nbr_slices)
    plt.plot(corpus_sizes, hapax_fractions)
    plt.xlabel('Corpus Size')
    plt.ylabel('Number of Hapax Words')
    plt.savefig('size_vs_hapax.png', dpi = 800)


def print_corpus_statistics(corpus):
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
    print('Number of unique bigrams: %d' % find_nbr_unique_bigrams(corpus))
    print('The unique bigrams make up %.1f%% of the corpus' % \
        (100*find_nbr_unique_bigrams_fraction(corpus)))
    print('Number of unique trigrams: %d' % find_nbr_unique_trigrams(corpus))
    print('The unique trigrams make up %.1f%% of the corpus' % \
        (100*find_nbr_unique_trigrams_fraction(corpus)))

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
    
    # make_hapax_plot(corpus, 30) #uncomment to make and save plot

if __name__ == "__main__":
    main()


