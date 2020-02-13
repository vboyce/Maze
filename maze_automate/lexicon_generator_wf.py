'''Functions related to building word to frequency lookups and lists of possible distractor words '''

import gzip
import csv
import math
import re
import json
from ast import literal_eval
import wordfreq

def make_word_list(output="word_list_wf.json", source="words.txt", exclude="exclude_wf.txt"):
    '''Makes a list of valid (distractor) words and writes to a json
    words are valid if they are in source, not in exclude,
    and consist only of lowercase alpha characters
    Arguments:
    output - location to write .json output (default is word_list.json)
    source - file with a list of words (default is copy of unix dictionary)
    exclude - file with a list of words to not include
    Return: none'''
    words = {}
    with open(source, "r") as f: #read dictionary
        for line in f:
            word = line.strip()
            if re.match("^[a-z]*$", word): #check for all lowercase alpha
                words[word] = 1
    f.close()
    if exclude is not None:
        with open(exclude, "r") as f: #remove words on exclude list
            for line in f:
                word = line.strip()
                words.pop(word, None)
    f.close()
    with open(output, "w") as f: #write to file
        json.dump(words, f)

def load_word_list(filename):
    '''loads a word_list created by make_word_list'''
    with open(filename, "r") as f:
        word_list = json.load(f)
    return word_list

 
def check_dist(out_distractor):
    '''Creates  a (length, freq_bin): list of valid distractors dictionary and writes to file
    Freq bins are floor of natural log of number of occurances in 1 billion words (expected)
    Argument: out_distractor - location to write to
    Returns: none'''
    good=load_word_list("word_list_wf.json")
    freq_dict=wordfreq.get_frequency_dict('en') #word frequencies as decimals
    distractor_dict={}
    for key in good: # cuts length off at 4, 15
        if len(key)<4: 
            word_length=4
        elif len(key)>15:
            word_length=15
        else:
            word_length=len(key)
        if key in freq_dict:
        #convert to natural log of number of expected occurances in 1 billion words
            freq=math.floor(math.log(freq_dict[key]*10**9)) 
            if freq>11:
                freq=11
            if freq<2:
                freq=2
            if (word_length, freq) in distractor_dict:
                distractor_dict[(word_length, freq)].append(key)
            else:
                distractor_dict[(word_length, freq)] = [key]
    with open(out_distractor, "w") as f:
        json.dump({str(k):v for k, v in distractor_dict.items()}, f)
    #for key in distractor_dict:
        #print(key[0],key[1], len(distractor_dict[key]))
    return
            
    
def load_distractor_dict(filename):
    '''loads a lexicon saved in a json format by make_lexicon'''
    with open(filename, "r") as f:
        obj = json.load(f)
    distractor_dict = {literal_eval(k):v for k, v in obj.items()}
    return distractor_dict
      
## Uncomment these lines to regenerate distractor word list      
#make_word_list()
#check_dist("distractor_list.json")

