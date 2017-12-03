# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 15:15:35 2017

@author: Rasmus
"""

import nltk
from nltk import ngrams
import pandas
import numpy as np


def brown_tagged_sents(genre):
    """Returns the tagged sentences of the given Brown category."""
    return nltk.corpus.brown.tagged_sents(categories=genre)

def brown_tagged_words(genre):
    return nltk.corpus.brown.tagged_words(categories=genre)

def print_brown_statistics(list_of_genres):
    df = pandas.DataFrame(columns=['Brown genre', 'POS tags', 'Sentences',
                                   'Words', 'Avg. sent. length', 
                                   'Avg. word length'])
    for genre in list_of_genres:
        tagged_sents = brown_tagged_sents(genre)
        tagged_words = brown_tagged_words(genre)
        word_lengths = [len(x[0]) for x in tagged_words]
        avg_w_len = np.mean(word_lengths)
        sentence_lens = [len(x) for x in tagged_sents]
        avg_s_len = np.mean(sentence_lens)
        tags = set([x[1] for x in tagged_words])
        results = {'Brown genre': genre, 'Sentences':len(tagged_sents),
                   'Words': len(tagged_words), 'Avg. word length': avg_w_len,
                   'POS tags': len(tags), 'Avg. sent. length': avg_s_len}
        df = df.append(results, ignore_index=True)
    print(df.to_string(index=False))


def print_common_tag_ngrams(genre, n, rows):
    tagged_sents = brown_tagged_sents(genre)
    
    freq_dist = nltk.FreqDist()
    for sentence in tagged_sents:
        tags = [x[1] for x in sentence]
        for ngram in ngrams(tags, n, pad_left=True, pad_right=True, 
                            left_pad_symbol="$", right_pad_symbol="$"):
            freq_dist[ngram] += 1

    N = freq_dist.N()
    cum_freq = 0
    tmp = round(6+0.8*n+4*n**0.5)
    header = ('{:<' + str(tmp) +'s}').format(str(n) + '-gram') #{:<'+ str(tmp) + 's}-gram \tFrequency\tCumulative frequency'
    header += 'Frequency\tCumulative frequency'
    print(header)    
    print('-----------------------------------------')
    for ngram, counts in freq_dist.most_common(rows):
        rel_freq = counts/N
        cum_freq += rel_freq
        ngram_str = ' '.join(ngram)
        print(('{:<' + str(tmp) +'s}{:.2%}    \t{:.2%}').format(ngram_str,
              rel_freq, cum_freq))


def split_sents(sents):
    return (sents[500:len(sents)], sents[0:500],)

def most_common_tag(sents):
    tags = []
    for i_sentence in sents:
        tags.extend([x[1] for x in i_sentence])
    freqs = nltk.FreqDist(tags)
    return freqs.most_common(1)[0][0]

def train_nltk_taggers(sents):
    default_tag = most_common_tag(sents)
    default_tagger = nltk.DefaultTagger(default_tag)
    afx_tagger = nltk.AffixTagger(sents, backoff=default_tagger)
    uni_tagger = nltk.UnigramTagger(sents, backoff=afx_tagger)
    bi_tagger = nltk.BigramTagger(sents, backoff=uni_tagger)
    tri_tagger = nltk.TrigramTagger(sents, backoff=bi_tagger)
    return default_tagger, afx_tagger, uni_tagger, bi_tagger, tri_tagger
    
def print_nltk_taggers_table(genre):
    train, test = split_sents(brown_tagged_sents(genre))  
    taggers = train_nltk_taggers(train)
    (default_tagger, afx_tagger, uni_tagger, bi_tagger, tri_tagger) = taggers
    print('Genre: ' + genre + '\tAccuracy\tErrors')
    print('---------------------------------------')
    accuracy = default_tagger.evaluate(test)
    print('deafult  \t{:.2%}  \t {:.2f}'.format(accuracy, 1.0/(1.0-accuracy)) 
            + ' words/error')
    accuracy = afx_tagger.evaluate(test)
    print('affix   \t{:.2%}  \t {:.2f}'.format(accuracy, 1.0/(1.0-accuracy)) 
            + ' words/error')
    accuracy = uni_tagger.evaluate(test)
    print('unigram  \t{:.2%}  \t {:.2f}'.format(accuracy, 1.0/(1.0-accuracy)) 
            + ' words/error')
    accuracy = bi_tagger.evaluate(test)
    print('bigram   \t{:.2%}  \t {:.2f}'.format(accuracy, 1.0/(1.0-accuracy)) 
            + ' words/error')
    accuracy = tri_tagger.evaluate(test)
    print('trigram  \t{:.2%}  \t {:.2f}'.format(accuracy, 1.0/(1.0-accuracy)) 
            + ' words/error')


def train_bigram_tagger(sents):
    return train_nltk_taggers(sents)[2]

def test_on_training_set(genre):
    train_sents, test_sents = split_sents(brown_tagged_sents(genre))
    tagger = train_bigram_tagger(train_sents)
    print('Training sentences\tAccuracy\tErrors    \tTesting sentences')
    print('------------------------------------------------------------------')
    accuracy = tagger.evaluate(test_sents)
    print(genre + '-train        \t{:.2%}'.format(accuracy) + 
            '\t      {:.2f}'.format(1.0/(1.0-accuracy))
            + ' words/error' + '\t' + genre + '-test')
    accuracy = tagger.evaluate(train_sents)
    print(genre + '-train        \t{:.2%}'.format(accuracy) + 
            '\t      {:.2f}'.format(1.0/(1.0-accuracy))
            + ' words/error' + '\t' + genre + '-train')

def test_different_genres(train_genre, test_genres):
    train_sents, _ = split_sents(brown_tagged_sents(train_genre))
    tagger = train_bigram_tagger(train_sents)    
    print('Training sentences\tAccuracy\tErrors    \tTesting sentences')
    print('------------------------------------------------------------------')
    for genre in test_genres:
        _, test_sents = split_sents(brown_tagged_sents(genre))
        accuracy = tagger.evaluate(test_sents)
        print(train_genre + '-train      \t{:.2%}'.format(accuracy) + 
                '\t      {:.2f}'.format(1.0/(1.0-accuracy))
                + ' words/error' + '\t' + genre + '-test')
    
def train_different_sizes(genre, sizes):
    train_sents, test_sents = split_sents(brown_tagged_sents(genre))
    nbr_train_sents = len(train_sents)
    tagger = train_bigram_tagger(train_sents)
    print('Training sentences\tAccuracy\tErrors    \tTesting sentences')
    print('------------------------------------------------------------------')
    for i_percentage in sizes:
        i_train_sents = train_sents[0:round(nbr_train_sents*i_percentage/100)]
        tagger = train_bigram_tagger(i_train_sents)
        accuracy = tagger.evaluate(test_sents)
        print(genre + '-train(' + str(i_percentage) + '%)     '
                + '\t{:.2%}'.format(accuracy) + 
                '\t      {:.2f}'.format(1.0/(1.0-accuracy))
                + ' words/error' + '\t' + genre + '-test')
        


def part1():
    print('== Part 1\n')
    print_brown_statistics(["fiction", "government", "news", "reviews"])
    print('')

def part2():
    print('== Part 2\n')
    print_common_tag_ngrams(["news"], 1, 10)
    print('')    
    print_common_tag_ngrams(["news"], 2, 10)
    print('')
    print_common_tag_ngrams(["news"], 3, 10)
    print('')

def part3():
    print('== Part 3\n')
    print_nltk_taggers_table('news')
    print('')

def part4():
    print('== Part 4\n')
    test_on_training_set('news')
    print('')
    test_different_genres("news", ["fiction", "government", "news", "reviews"])
    print('')
    train_different_sizes("news", [100, 75, 50, 25])
    print('')

if __name__ == '__main__':
    part1()
    part2()
    part3()
    part4()
