
# notes for gmaze automator

#take google ngram files (as zips) and turn into dictionary

# can just remove all capitilized words?, and de-pos tag
# come up with sane cutoff for threshold

import gzip
import csv
import math
import re
import pickle

def good_word(word,count):
    '''determines whether the "word" is actually a word we want
    '''
    # should eventually do more checking
    threshold=1000
    if count>=threshold: #common enough
        word_fixed=word.split("_")[0]
        if re.match("^[a-zA-Z'-]+$",word_fixed):
            if len(word_fixed)>0:
                return (word_fixed.lower())
    return False
    
def parse_files():
    '''builds a dictionary with words:frequency counts'''
    unigram_freq={}
    suffixes=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
          "u", "v", "w", "x", "y", "z"]
    prefix="../../unigram/googlebooks-eng-all-1gram-20120701-"
    postfix=".gz"
    for i in range(len(suffixes)):    
        a=""
        count=0
        with gzip.open(prefix+suffixes[i]+postfix, "rt") as f:
            if a=="":
                print(suffixes[i])
            for line in csv.reader(f, delimiter="\t"):
                if (a==line[0]): #same as prior line
                    count+=int(line[2])
                else: #looking at a new word
                    check=good_word(a,count)
                    if (check!=False):
                        if check in unigram_freq:
                            unigram_freq[check]+=count
                        else:
                            unigram_freq[check]=count
                    a=line[0]
                    count=int(line[2])
    return(unigram_freq)
        
        
def make_lexicon(unigram):
    '''takes the output of parse_files, returns 2 dicts
    forward lookup is word:floor log2 freq (only words with log2>=13 included)
    backward lookup is (len,floor log2 freq):[word list] (same cutoffs)
    '''
    uni_good={}
    lexicon={}
    for key in unigram:
        freq=math.floor(math.log(unigram[key],2))
        if freq>=13:
            uni_good[key]=freq
            if (len(key),freq) in lexicon:
                lexicon[(len(key),freq)].append(key)
            else:
                lexicon[(len(key),freq)]=[key]
    return(lexicon,uni_good)
    


def save_things(filename1, filename2):
    '''builds a lexicon as a dictionary and
saves it as a pickled file to filename'''
    lexicon, unigram_freq=make_lexicon(pickle.load(open("uni_bad.p", "rb")))
    pickle.dump(lexicon, open(filename1, "wb"))
    pickle.dump(unigram_freq, open(filename2, "wb"))
    return

def load_dict(filename):
    '''loads a lexicon or unigram_freq saved in a pickled format by make_lexicon'''
    dictionary=pickle.load(open(filename, "rb"))
    return dictionary
