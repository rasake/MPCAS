###################
## Helper functions


# get the first item of a list, tuple, string, ... anything that has indices
def fst(indexable):
    return indexable[0]

# get the second item of a list, tuple, string, ... anything that has indices
def snd(indexable):
    return indexable[1]

# print the output of the zipf nicely
def prettyprint(rank, word, freq, expected):
    if len(word) < 2:
        pad = "\t\t"
    else: 
        pad = "\t"
    print("#%02d: %s %s %d  %d" % (rank, word, pad, freq, expected)) 

## End helper funs
##################


#####################
## The Zipf function!

def zipf(document):
    """Takes a document, which we assume has been tokenised already.
    Returns a list of 4-tuples (rank, word, frequency, expected_frequency)."""
    
    # create the frequency distribution using a dictionary
    freqs = {}
    for word in document:
        if word in freqs:
            freqs[word] += 1
        else:
            freqs[word] = 1

    # sort it by value in reverse order
    # we use the helper function `snd' as the key
    # example data in top_freqs: [("the",500), ("a",450), ...]
    top_freqs = sorted(freqs.items(), key=snd, reverse=True)


    # 1st line: create a range from 1 to amount of tokens: e.g. 1-6132
    # 2nd line: for each (word,freq) pair in top_freqs, get the word
    # 3rd line: for each (word,freq) pair in top_freqs, get the freq
    ranks = list(range(1,len(top_freqs)+1))
    words = [word for (word,freq) in top_freqs]
    freqs = [freq for (word,freq) in top_freqs]

    # save the highest frequency in a variable
    # make it float so that division works
    highest_freq = float(freqs[0])
    
    # calculate the expected frequency for each word.
    # simply divide the highest frequency by the rank.
    # e.g. the expected frequency for the 315st ranked word is
    #     highest_freq
    #     ------------
    #         315
    expected_freqs = [(highest_freq / rank) for rank in ranks]

    # Finally, return the result!
    # zip takes n lists as an argument, and returns a list of n-tuples:
    # e.g. zip(['a','b'], [1,2]) returns [('a',1), ('b',2)].
    # 2017: added list() in order to make it python3-compatible
    return list(zip(ranks, words, freqs, expected_freqs))



###########################
## Let's test our function!

if __name__ == "__main__":    

    text = "this is some text, replace with your own, this is way too short!"

    print("#n: <word> \t freq  expected")
    print("-------------------------------")
    for r,w,f,ef in zipf(text)[:10]: # change if you want more/less items
        prettyprint(r,w,f,ef)
