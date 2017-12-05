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
    """ Returns a Brill tagger rule Template for tags on the postions specified
    by the boundaries."""
    return Template(*[Pos(b) for b in boundaries])

def word_template(*boundaries):
    """ Returns a Brill tagger rule Template for words on the postions specified
    by the boundaries. """
    return Template(*[Word(b) for b in boundaries])


def my_rule_templates():
     """ Returns a list of Templates for the Brill tagger. """
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
    """ Returns a Hidden Markov Model tagger trained on the train_sents. """
    priorsFD = nltk.FreqDist([x[0][1] for x in train_sents])
    priorsPD = nltk.MLEProbDist(priorsFD)
    
    outputsCFD = nltk.ConditionalFreqDist()
    transitionsCFD = nltk.ConditionalFreqDist()
    symbols = set([])
    states = set([])
    for i_sentence in train_sents:
        prev_tag = None
        for (word, tag) in i_sentence:
            symbols.add(word)
            states.add(tag)
            outputsCFD[tag][word] += 1
            if prev_tag != None:
                transitionsCFD[prev_tag][tag] += 1
            prev_tag = tag
    tag_types = list(states)
    word_types = list(symbols)
    transitionsCPD = nltk.ConditionalProbDist(transitionsCFD, probdist, bins=len(tag_types))
    outputsCPD = nltk.ConditionalProbDist(outputsCFD, probdist, bins=len(word_types))
    
    tagger = nltk.HiddenMarkovModelTagger(word_types, tag_types, transitionsCPD, outputsCPD, priorsPD)
    return tagger

def train_hmm_tagger_simple(train_sents, probdist):
    """ Trains an HMM tagger using the built in HiddenMarkovModelTrainer class. """
    tag_types = list(set(tag for sentence in train_sents for (word, tag) in sentence))
    word_types = list(set(word for sentence in train_sents for (word, tag) in sentence))
    trainer = nltk.tag.HiddenMarkovModelTrainer(tag_types, word_types)
    return trainer.train_supervised(train_sents, estimator = probdist)


def part1():
    """ Trains and evaluates a Brill tagger, prints results to terminal. """
    print('== Part 2\n')
    news_train, news_test = lab2.split_sents(lab2.brown_tagged_sents('news'))
    (_default, _affix, unitagger, _bi, _tri) = lab2.train_nltk_taggers(news_train)
    baseline_tagger = unitagger
    trainer = nltk.BrillTaggerTrainer(baseline_tagger, my_rule_templates())
    tagger = trainer.train(news_train, max_rules=1000)
    result = tagger.evaluate(news_test)
    print ("Brill tagger with %d rules, evaluated on the %s genre: %.2f%% accuracy" %
           (len(tagger.rules()), "news", 100.0 * result))

def part2():
    """ Trains and evaluates a few different HMM taggers, prints results to terminal. """
    print('== Part 2\n')
    news_train, news_test = lab2.split_sents(lab2.brown_tagged_sents('news'))
    
    probdist = lambda fd, bins: nltk.WittenBellProbDist(fd, bins)
    tagger = train_hmm_tagger(news_train, probdist)
    result = tagger.evaluate(news_test)
    print ("HMM tagger, WittenBellProbDist, %.2f%% accuracy" % ( 100.0 * result))
    
    probdist = lambda fd, bins: nltk.SimpleGoodTuringProbDist(fd, bins)
    tagger = train_hmm_tagger(news_train, probdist)
    result = tagger.evaluate(news_test)
    print ("HMM tagger, SimpleGoodTuringProbDist, %.2f%% accuracy" % ( 100.0 * result))
    
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

if __name__ == '__main__':
    part1()
    part2()
