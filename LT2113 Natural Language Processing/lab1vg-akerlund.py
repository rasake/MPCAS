# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:46:55 2017

@author: Rasmus
"""

import sys
import os.path
import numpy as np
from operator import itemgetter
from urllib import request
from bs4 import BeautifulSoup
import nltk
import re

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

def tokenize_corpus(text):
    """Don't forget the docstring!"""
    return nltk.regexp_tokenize(text, TOKEN_REGEXP)

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

def find_nbr_bigrams(corpus):
    """ Returns the total number of bigrams in the corpus. """
    tokens = tokenize_corpus(corpus)
    bigrams = list(nltk.bigrams(tokens))
    return len(bigrams)

def find_nbr_unique_bigrams(corpus):
    """ Returns the number of unique bigrams in the corpus. """
    tokens = tokenize_corpus(corpus)
    bigrams = nltk.bigrams(tokens)
    freqs = nltk.FreqDist(bigrams)
    nbr_unique = 0
    for sample in freqs:
        if freqs[sample] == 1:
            nbr_unique += 1
    return nbr_unique

def find_nbr_unique_bigrams_fraction(corpus):
    """ Returns the fraction of bigrams in the corpus that unique. """
    return find_nbr_unique_bigrams(corpus) / find_nbr_bigrams(corpus)

def find_nbr_trigrams(corpus):    
    """ Returns the total number of trigrams in the corpus. """
    tokens = tokenize_corpus(corpus)
    trigrams = list(nltk.trigrams(tokens))
    return len(trigrams)

def find_nbr_unique_trigrams(corpus):
    """ Returns the number of unique trigrams in the corpus. """
    tokens = tokenize_corpus(corpus)
    trigrams = nltk.trigrams(tokens)
    freqs = nltk.FreqDist(trigrams)
    nbr_unique = 0
    for sample in freqs:
        if freqs[sample] == 1:
            nbr_unique += 1
    return nbr_unique

def find_nbr_unique_trigrams_fraction(corpus):
    """ Returns the fraction of trigrams in the corpus that unique. """
    return find_nbr_unique_trigrams(corpus) / find_nbr_trigrams(corpus)

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
    print('Number of unique bigrams: %d' % find_nbr_unique_bigrams(corpus))
    print('The unique bigrams make up %.1f%% of the corpus' % \
        (100*find_nbr_unique_bigrams_fraction(corpus)))

def download_wikipedia_article(article_name):
    """ Returns the raw text from a Wikipedia article. """
    url = 'http://en.wikipedia.org/w/index.php?title=' + '+'.join(article_name.split(' ')) + '&action=raw'
    response = request.urlopen(url)
    raw_text = response.read().decode('utf8')
    return raw_text

def remove_xml_html(text):
    """ Removes xml/html tags from a string. """
    soup = BeautifulSoup(text, 'lxml')
    return soup.get_text()

def remove_simple_wiki_links(text):
    """ Removes the brackets around simple Wikipedia article links. """
    simple_link_regex = '\[\[[a-zA-Z ]+\]\]'
    indices_to_remove = []
    for match in re.finditer(simple_link_regex, text):
        indices_to_remove.append(match.start())
        indices_to_remove.append(match.start()+1)
        indices_to_remove.append(match.end()-1)
        indices_to_remove.append(match.end())
    for index in reversed(indices_to_remove):
        if index > 0:
            text = text[0:index-1] + text[index: len(text)]
        else:
            text = text[1:len(text)]
    return text

def remove_inline_references(text):
    """ Removes Wikipedia inline references. """
    return re.sub('<ref>.*</ref>', '', text)

def remove_wiki_markup(text):
    """ Removes Wikipedia markup. """
    new_text = remove_simple_wiki_links(text)
    regex_lst = ['\[\[Category:[a-zA-Z ]*\]\]',
                 '\{\{Refbegin\}\}(.|\n)*\{\{Refend\}\}', #Reference section
                 '\{\{About\|.*\}\}', # About section, not really part of the article
                 '==See also==(.*\n)*',
                 '=+[a-zA-Z0-9 \-(),]+=+', # Headers
                 '[*]', # Bullet points,
                 '\[\[:*(File|Media|Image)(.)*\]\]',  # Images etc
                 'https*://[a-zA-Z0-9./-]+ ', # hyperlinks
                 r'\{\{(\n|[^{}])*}\}', # citations and more
                 r'\{\|(\n|[^{}])*\|\}', # citations and more
                 '\[\[[a-zA-Z #()-_]*\|', '\[|\]', # overlayed links 
                 r'^;',
                 '  *'] #multiple whitespaces
    for rgx in regex_lst:
        new_text = re.sub(rgx, ' ', new_text)
    new_text = re.sub(r'^\u003B *', '', new_text, flags=re.MULTILINE)
    if len(text) != len(new_text): # Recursive call to get rid of nested tags
        return remove_wiki_markup(new_text)
    else:
        return new_text

def clean_wikipedia_articel(raw_text):
    """ Removes xml/html and Wikipedia mark up from a Wikipedia article. """
    clean_text = remove_inline_references(raw_text)
    clean_text = remove_xml_html(clean_text)
    clean_text = remove_wiki_markup(clean_text)
    return clean_text

if __name__ == '__main__':
    
    # If incorrect number of command line args, print helpful message    
    if len(sys.argv) != 2: 
        this_file = os.path.basename(sys.argv[0])
        exit_message = 'Usage: python ' + this_file + \
            r' "The title of any Wikipedia article"'
        exit(exit_message)
    
    article_name = sys.argv[1]
    raw_text = download_wikipedia_article(article_name)
    cleaned_text = clean_wikipedia_articel(raw_text)
    
    print('Statistics for the Wikipeda article ' + r'"' + article_name + r'"')
    print('-----------------------------------------------------------------')
    print_corpus_statistics(cleaned_text)
    #print(cleaned_text)
