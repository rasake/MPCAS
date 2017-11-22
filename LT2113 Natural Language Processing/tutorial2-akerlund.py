# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import gutenberg
import re
import zipf
import matplotlib.pyplot as plt
import seaborn # Makes graphs prettier


###############################
######  Q1 ZIPF'S LAW  ########
"""
Zipf's law states that the number of occurencies of a word type in a corpus
is inversely proportional to its rank. The practical effect of this is that
even though a few common word types makes up a large portion of the corpus, 
so do rare words, meaning that even if after studying most of the corpus you
will still continue to find new words.
"""
# Investigating the rank-frequency relation for a few corpora
texts = {'Emma, J. Austen': gutenberg.words('austen-emma.txt'),
         'Hamlet, Shakespeare': gutenberg.words('shakespeare-hamlet.txt'),
         'Alice in Wonderland, L. Caroll': gutenberg.words('carroll-alice.txt'),
         'Moby Dick, H. Melville': gutenberg.words('melville-moby_dick.txt')}
legend = []
for title, words in texts.items():
    legend.append(title)
    corpora_size = len(words)
    results = zipf.zipf(words)
    rank = [x[0] for x in results]
    rel_freq = [x[2]/corpora_size for x in results]
    plt.loglog(rank, rel_freq)
    plt.xlabel('Rank')
    plt.ylabel('Relative Frequency')
plt.legend(legend)
plt.title('Zipfs law')
plt.savefig('ZipfsLaw.png', dpi=800)

"""
Looking at the graphs, it appears they follow a straight line in the loglog 
domain, in other words it seems Zipf's law holds pretty well. However the,
the tail is sometimes falling off a bit, indicating that Zipf's law may 
overestimates the frequency of the very rare words slightly.
"""


####################################
######  Q2 LANGUAGE MODELS  ########
"""
The purpose of a statistical language models is to estimate the probablity of
words and word sequences, and they are used to resolve ambiguities in language.
For example, if speech recognition system is to distinguish between a speaker
saying "won" or "one", it may use a language model, to conclude that if the previous word
is "she", the speaker is more likely saying "she won" than "she one".

Now, in this task we consider three scenarions:

----- Scenario 1 -----
Assumption: The true language is described by the 20-grams derived from all
English ever written or spoken. So, in this reality, the 'true' language is 
basically identical to actual English (statistically) since 20 words is enough
for close to all sentences.

What happens if we use the uniform model to describe this language? Well, the 
vocabulary of the uniform model constists of the 100 most common English words,
and they would also be very common in the 'true' language of this scenario, so
that's a good start. However, this model does not take the context into account,
it would for example deem "him tomorrow I meet will" as likely as "I will meet
him tomorrow". In an application such as suggesting the next word in a text 
messages this would be useless since it would just suggest any of the 100 most 
common words randomly and miss really obvious stuff, like if I write "See you"
the next word in the 'true' language is very likely to be "tomorrow", "later" 
or "tonight", but the uniform model would only have a couple of percents chance
to guess right (assuming the words are even in the 100-word vocabulary).

The dog+ model would be crap of course, it would just guess "dog" all the time.


----- Scenario 2 -----
Assumption: The 'true' language consists of 100 words (the most common in 
English) and all are equally likely.

If we use a the 20-gram model trained on English ever written or spoken, the
probabilitites it had learnt would not be correct. For instance, it woul 
assign a very low, or possible zero, probabability to the sequence "she I will 
other think people and", whereas in the 'true' language this sequence is equally 
likely as any other sequence with the same length.

Again, the dog+ model would be useless.


----- Scenario 3 -----
Assumption: The 'true' language consists of any number of repitions of "dog".

In this case, none of the other two models would describe any of the statistical
properties of the language. However, "dog" woul be in the vocabulary of the
20-gram model but not in the uniform model, so if we are doing speech recognition
th 20-gram model might kind of work, because there is not really any other words
that sound like dog as far I as know, so then there is no ambiguity to resolve,
but if the true language is just 'dog dog dog' what is the point of speech
recognition at all?
"""



##########################################
######  Q3 PART OF SPEECH TAGGING ########

##### a) Look-up tables #####
"""
One disadvantage with the look-up tagger is that it doesn't take the context 
into account, since the tag for a given word is fix, it can't distiguish 
between the same word having different functions. For example, the sentence 
"I saw a saw" contains two instances of the word "saw", the first being a verb
and the second being a noun, and a look-up tagger is bound to get a least one 
of them wrong.

Another disadvantage is that a look-up tagger cannot handle new words that are
absent in the look up table.
"""



###### b) POS tagging using suffixes ######
## PLEASE OBSERVE THESE REGEXES ASSUMES TOKENIZED INPUT ##
text = 'I am the whalrus, begging for attention, please witness my sadness.'
tokens = nltk.word_tokenize(text)

regex_vbg = '[A-Za-z][a-z]+ing'
# This finds VBG such as running, showering etc.
# This would incorrectly tag some adjectives like outstanding.
# Also, some words are either VBG or JJ depending on the context,
# e.g. "He is a stunning gentleman" vs "The police is stunning him"
print([x for x in tokens if re.match(regex_vbg, x)])

regex_nn_1 = '[A-Za-z][a-z]+tion'
# This finds nouns (NN) such as running, showering etc.
# This would incorrectly tag some adjectives like outstanding.
# Also, some words are either VBG or JJ depending on the context,
# e.g. "He is a stunning gentleman" vs "The police is stunning him"
print([x for x in tokens if re.match(regex_nn_1, x)])

regex_nn_2 = '[A-Za-z][a-z]+ness'
# This finds nouns (NN) such as happiness, madness etc.
# The only example on words that would be incorrectly tagged I 
# can think of is the verb "witness"
print([x for x in tokens if re.match(regex_nn_2, x)])



##### c) HMM tagger #####
prob_N_given_DET = 3/3
prob_fish_given_N = 1/3
prob_noun = prob_N_given_DET * prob_fish_given_N # = 1/3
prob_V_given_DET = 0/1
prob_fish_given_V = 1/2
prob_verb = prob_V_given_DET * prob_fish_given_V # = 0
"""
The tagger will choose the tag which maximizes the probability.
Ergo: "fish" will be tagged as a noun in the phrase "a fish"
"""
