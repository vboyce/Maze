
# notes for gmaze automator

#take google ngram files (as zips) and turn into dictionary

# can just remove all capitilized words?, and de-pos tag
# come up with sane cutoff for threshold

import gzip
import csv
import math
import re
import json
from ast import literal_eval

def good_word(word,count):
    '''determines whether the "word" is actually a word we want
    '''
    threshold=1000
    if count>=threshold: #common enough
        word_fixed=word.split("_")[0]
        if re.match("^[a-zA-Z'-]+$",word_fixed):
            if len(word_fixed)>0:
                return (word_fixed)
    return False
    
def parse_files():
    '''builds a dictionary with words:frequency counts'''
    unigram_freq={}
    suffixes=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
             "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
             "u", "v", "w", "x", "y", "z"]
    prefix="../unigram/googlebooks-eng-all-1gram-20120701-"
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
                    if (check!=False): #it's a good word 
                        if check.lower() in unigram_freq: # base entry already exists
                            if check in unigram_freq[check.lower()][0]: #exact entry exists
                                    location=unigram_freq[check.lower()][0].index(check) #find it
                                    unigram_freq[check.lower()][1][location]+=count #add to it
                            else: #base entry, but not cased entry
                                unigram_freq[check.lower()][0].append(check) #make one
                                unigram_freq[check.lower()][1].append(count)
                        else: #no entry, so make one
                            unigram_freq[check.lower()]=[[check],[count]]
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
        #for each word form, find the plurality form
        #sum up occurances and count them all as being plurality form (wrt capitalization)
        common_index=unigram[key][1].index(max(unigram[key][1])) 
        common_form=unigram[key][0][common_index]
        total_count=sum(unigram[key][1])
        freq=math.floor(math.log(total_count,2))
        if len(key)<3:
            word_length=3
        elif len(key)>15:
            word_length=15
        else:
            word_length=len(key)
        if freq>25: 
            freq=25
        if freq>=13:
            uni_good[common_form]=freq
            if (word_length,freq) in lexicon:
                lexicon[(word_length,freq)].append(common_form)
            else:
                lexicon[(word_length,freq)]=[common_form]
    return(lexicon,uni_good)
    


def save_things(filename1, filename2):
    '''builds a lexicon as a dictionary and
saves it as a  json file to filename'''
    lexicon, unigram_freq=make_lexicon(parse_files())
    with open(filename1, "w") as f:
        json.dump({str(k):v for k, v in lexicon.items()}, f)
    with open(filename2, "w") as f:
        json.dump(unigram_freq, f)
    return

def load_lexicon(filename):
    '''loads a lexicon saved in a json format by make_lexicon'''
    with open(filename, "r") as f:
        obj=json.load(f)
    lexicon={literal_eval(k):v for k, v in obj.items()}
    return lexicon

def load_unigram(filename):
    '''loads a unigram_freq saved in a json format by make_lexicon'''
    with open(filename, "r") as f:
        unigram=json.load(f)
    return unigram
