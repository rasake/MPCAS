# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:45:59 2017

@author: Rasmus
"""


# module imports
import nltk


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

if __name__ == "__main__":
    nr_files = 50
    corpus_text = get_corpus_text(nr_files)
    print(type(corpus_text))
    gold_tokens = get_gold_tokens(nr_files)
    tokens = tokenize_corpus(corpus_text)
    evaluate_tokenization(tokens, gold_tokens)
    
"""
Corpus statistics

Use the tokenized corpus to answer the following questions:

How big is the corpus in terms of the number of word tokens and in terms of word types?
What is the average word token length?
What is the longest word length and what words have that length?
How many hapax words are there? How many percent of the corpus do they represent?
(For this question and the questions below, by corpus size, we mean the number of tokens)
Which are the 10 most frequent words? How many percent of the corpus do they represent?
Divide the corpus in 10 slices of equal sizes: s[0]...s[9].
How many hapaxes are there in each of the slices in terms of percentage of the subcorpus?
Now look at subcorpora of increasing size: s[0], s[0]+s[1], s[0]+s[1]+s[2], and so on, until you have reconstructed the complete corpus. How many hapaxes are there in each of these subcorpora? How much is it in each case in terms of a percentage of the subcorpus?
Draw the results from question 6 in a graph.
How many unique word bigrams are there in the corpus? How many percent do they represent of all bigrams?
How many unique trigrams are there? How many percent of all trigrams do they represent?
Implemented each of these questions as a function that takes the corpus as its argument and returns the answer:

"""
