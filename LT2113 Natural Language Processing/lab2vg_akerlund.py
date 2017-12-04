# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 10:26:35 2017

@author: Rasmus
"""

import nltk
from nltk.tag.brill import Word
from nltk.tag.brill import Pos
from nltk.tag.brill import Template

import lab2_akerlund as lab2


def tag_template(*boundaries):
    return Template(*[Pos(b) for b in boundaries])

def word_template(*boundaries):
    return Template(*[Word(b) for b in boundaries])



def my_rule_template():
     return [tag_template((-1,-1)),
        tag_template((-2,-1)),
        tag_template((1,1)),
        tag_template((-3,-1)),
        tag_template((-1,-1),(1,1)),
        word_template((1,1)),
        word_template((-1,-1)),
        word_template((-2,-1)),
        word_template((-3,-1)),
        word_template((-1,-1),(1,1)),
        Template(Pos([-1]), Word([-2]))]



def train_hmm_tagger(train_sents, probdist):
    tagged_words = []
    tags = []
    words = []
    tag_bigrams = []
    for i_sentence in train_sents:
        tagged_words.extend([(x[1], x[0]) for x in i_sentence])
        i_tags = [x[1] for x in i_sentence]
        tags.extend(i_tags)
        words.extend([x[0] for x in i_sentence])
        for bigram in nltk.bigrams(i_tags):#, pad_left=True, pad_right=True, 
                            #left_pad_symbol="$", right_pad_symbol="$"):
            tag_bigrams.append((bigram[1], bigram[0]))
    tag_types = list(set(tags))
    word_types = list(set(words))
    transitionsCFD = nltk.ConditionalFreqDist(tag_bigrams)  
    outputsCFD = nltk.ConditionalFreqDist(tagged_words)
    outputsCPD = nltk.ConditionalProbDist(outputsCFD, probdist, bins=len(set(tagged_words)))
    transitionsCPD = nltk.ConditionalProbDist(transitionsCFD, probdist, bins=len(set(tag_bigrams)))
    priorsFD = nltk.FreqDist([x[0][1] for x in train_sents])
    priorsPD = nltk.MLEProbDist(priorsFD)
    tagger = nltk.HiddenMarkovModelTagger(word_types, tag_types, transitionsCPD, outputsCPD, priorsPD)
    return tagger

def find_nbr_missing_items(setA, setB):
    """ Returns the number of items that are in setB, but not in setA. """
    return len([x for x in setB if x not in setA])

def extract_words_n_tags(tagged_sentences):
    """ Return a tuple with (tagged words, words, tags). """
    tagged_words = []
    tags = []
    words = []
    for i_sentence in tagged_sentences:
        tagged_words.extend(i_sentence)
        tags.extend([x[1] for x in i_sentence])
        words.extend([x[0] for x in i_sentence])
    return (tagged_sentences, words, tags)


def part1():
    news_train, news_test = lab2.split_sents(lab2.brown_tagged_sents('news'))
    (_default, _affix, unitagger, _bi, _tri) = lab2.train_nltk_taggers(news_train)
    baseline_tagger = unitagger
    trainer = nltk.BrillTaggerTrainer(baseline_tagger, my_rule_template())
    tagger = trainer.train(news_train, max_rules=1000)
    result = tagger.evaluate(news_test)
    print ("Brill tagger with %d rules, evaluated on the %s genre: %.2f%% accuracy" %
           (len(tagger.rules()), "news", 100.0 * result))

def part2():
    news_train, news_test = lab2.split_sents(lab2.brown_tagged_sents('news'))
    
    probdist = lambda fd, bins: nltk.WittenBellProbDist(fd, bins)
    tagger = train_hmm_tagger(news_train, probdist)
    result = tagger.evaluate(news_test)
    print ("HMM tagger, WittenBellProbDist, %.2f%% accuracy" % ( 100.0 * result))
    
    """
    probdist = lambda fd, bins: nltk.SimpleGoodTuringProbDist(fd, bins)
    tagger = train_hmm_tagger(news_train, probdist)
    result = tagger.evaluate(news_test)
    print ("HMM tagger, SimpleGoodTuringProbDist, %.2f%% accuracy" % ( 100.0 * result))
    """
    probdist = lambda fd, bins: nltk.LaplaceProbDist(fd, bins)
    tagger = train_hmm_tagger(news_train, probdist)
    result = tagger.evaluate(news_test)
    print ("HMM tagger, LaplaceProbDist, %.2f%% accuracy" % ( 100.0 * result))
     
    probdist = lambda fd, bins: nltk.LidstoneProbDist(fd, 0.1, bins)
    tagger = train_hmm_tagger(news_train, probdist)
    result = tagger.evaluate(news_test)
    print ("HMM tagger, LidstoneProbDist with gamma=0.1, %.2f%% accuracy" % ( 100.0 * result))

    probdist = lambda fd, bins: nltk.LidstoneProbDist(fd, 0.01, bins)
    tagger = train_hmm_tagger(news_train, probdist)
    result = tagger.evaluate(news_test)
    print ("HMM tagger, LidstoneProbDist with gamma=0.01, %.2f%% accuracy" % ( 100.0 * result))
    
    
    probdist = lambda fd, bins: nltk.LidstoneProbDist(fd, 0.001, bins)
    tagger = train_hmm_tagger(news_train, probdist)
    result = tagger.evaluate(news_test)
    print ("HMM tagger, LidstoneProbDist with gamma=0.001, %.2f%% accuracy" % ( 100.0 * result))
        
    """    
    print('\n Some information about the training and test set')   
    (_, train_words, train_tags) = extract_words_n_tags(news_train)    
    (_, test_words, test_tags) = extract_words_n_tags(news_test)   
    nbr_missing_tokens = len([x for x in test_words if x not in train_words])
    print('Percentage of word tokens that are in the test sentences but not in the ' +
        'training set: ' + str(nbr_missing_tokens/len(test_words)))
    """

if __name__ == '__main__':
    part2()
