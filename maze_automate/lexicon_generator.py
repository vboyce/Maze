'''Functions related to building word to frequency lookups and lists of possible distractor words '''

import gzip
import csv
import math
import re
import json
from ast import literal_eval

def make_word_list(output="word_list.json", source="words.txt", exclude="exclude.txt"):
    '''Makes a list of valid (distractor) words and writes to a json
    words are valid if they are in source, not in exclude,
    and consist only of lowercase alpha characters
    Arguments:
    output - location to write .json output (default is word_list.json)
    source - file with a list of words (default is copy of unix dictionary)
    exclude - file with a list of words to not include
    Return: none'''
    words = set()
    with open(source, "r") as f: #read dictionary
        for line in f:
            word = line.strip()
            if re.match("^[a-z]*$", word): #check for all lowercase alpha
                words.add(word.lower())
    f.close()
    if exclude is not None:
        with open(exclude, "r") as f: #remove words on exclude list
            for line in f:
                word = line.strip()
                words.remove(word.lower())
    f.close()
    with open(output, "w") as f: #write to file
        json.dump(words, f)

def override_freq(filename="contractions.csv"):
    '''Creates a dictionary of words and frequencies
    Used to manually change frequency for words where the automatic frequency
    is wrong (ie. contractions, due to how google books parses things)
    Arguments:
    filename = None or a file in csv format with word, new frequency.
    Frequency should be floor(log 2 frequency).'''
    words = {}
    if filename is not None:
        with open(filename, "r") as f:
            for row in csv.reader(f, delimiter=","):
                words[row[0]] = int(row[1])
    return words

def load_word_list(filename):
    '''loads a word_list created by make_word_list'''
    with open(filename, "r") as f:
        word_list = json.load(f)
    return word_list

def good_word(word, count, threshold = 1000):
    '''Determines if a word should be included
    Cleans it up as needed
    Chops off POS tags (after _ in google corpus)
    Then keeps words if they consist only of letters, apostrophe and comma
    Arguments:
    word = a word
    count = number of occurances
    Returns: either the word (minus POS tag) or False
    '''
    #threshold = 1000
    if count >= threshold: #common enough
        word_fixed = word.split("_")[0]
        if re.match("^[a-zA-Z'-]+$", word_fixed):
            if word_fixed:
                return word_fixed
    return False

def parse_files(filename="unigram_raw.json"):
    '''builds a dictionary with words:frequency counts and writes it to a json file
    Includes all words from the googlebooks corpus
    that meet criteria in good_word
    Arguments:
    filename= file to write to
    Returns none
    Saves a dictionary with lowercase words as keys and
    value as a list of two lists, one of words (cased)
    and one of counts for those cased versions to json file'''
    unigram_freq = {}
    suffixes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    prefix = "../unigram/googlebooks-eng-all-1gram-20120701-"
    postfix = ".gz"
    for char in suffixes:
        test_word = ""
        count = 0
        with gzip.open(prefix+char+postfix, "rt") as f:
            if test_word == "":
                print(suffixes[i])
            for line in csv.reader(f, delimiter="\t"):
                if test_word == line[0]: #same as prior line
                    count += int(line[2])
                else: #looking at a new word
                    check = good_word(test_word, count)
                    if check: #it's a good word
                        if check.lower() in unigram_freq: # base entry already exists
                            if check in unigram_freq[check.lower()][0]: #exact entry exists
                                location = unigram_freq[check.lower()][0].index(check) #find it
                                unigram_freq[check.lower()][1][location] += count #add to it
                            else: #base entry, but not cased entry
                                unigram_freq[check.lower()][0].append(check) #make one
                                unigram_freq[check.lower()][1].append(count)
                        else: #no entry, so make one
                            unigram_freq[check.lower()] = [[check], [count]]
                    test_word = line[0]
                    count = int(line[2])
    with open(filename, "w") as f:
        json.dump(unigram_freq, f)

def load_raw_unigram(filename):
    '''loads raw ungram frequencies made by parse_files'''
    with open(filename, "r") as f:
        raw_unigram = json.load(f)
    return raw_unigram

def make_lexicon(unigram, word_list, alterations):
    '''Makes useable look-up dictionaries
    Arguments:
    unigram - from parse_files, a dictionary of words
    to cased versions and raw frequencies
    word_list - a list of words word-like enough to be distractors
    alterations - a dictionary of words to floor log2 frequencies
    containing any needed manual changes
    Returns:
    lexicon is a dictionary of (len, floor log2 freq):[word list]
    (only words with log2> = 13 that are also in the word_list are included)
    uni_good is word:floor log2 freq
    (only words with log2> = 13 included, alterations applied)
    '''
    uni_good = {}
    lexicon = {}
    for (key, value) in unigram.items():
        #for each word form, find the plurality form
        #sum up occurances and count them all as being plurality form (wrt capitalization)
        common_index = value[1].index(max(value[1]))
        common_form = value[0][common_index]
        total_count = sum(value[1])
        freq = math.floor(math.log(total_count, 2))
        if common_form in alterations: #check if it needs to be modified
            freq = alterations[common_form]
        word_length = max(3, min(len(key), 15))
        freq = min(freq, 25)
        if freq >= 13:
            uni_good[common_form] = freq
            if common_form in word_list:
                if (word_length, freq) in lexicon:
                    lexicon[(word_length, freq)].append(common_form)
                else:
                    lexicon[(word_length, freq)] = [common_form]
    return(lexicon, uni_good)

def save_things(raw_words="unigram_raw.json", word_list="word_list.json", override="contractions.csv", out_lexicon="lexicon.json", out_unigram="unigram.json"):
    '''Takes files for raw unigram frequencies (from parse_files),
    raw word list (from make_word_list), and file of words to override (or None).
    Builds forward and reverse look-up dictionaries for words to frequencies/length
    And saves them in json format
    Arguments:
    raw_words- json file output from parse_files
    word_list -json file output from make_word_list
    override - csv formatted file with words and log2 frequencies to override with (or None)
    out_lexicon - json file to save the lexicon (freq, length) --> word list
    out_unigram - word to frequency look up
    Returns none
    Saves outputs to out_lexicon and out_unigram'''
    lexicon, unigram_freq = make_lexicon(load_raw_unigram(raw_words), load_word_list(word_list), override_freq(override))
    with open(out_lexicon, "w") as f:
        json.dump({str(k):v for k, v in lexicon.items()}, f)
    with open(out_unigram, "w") as f:
        json.dump(unigram_freq, f)

def load_lexicon(filename):
    '''loads a lexicon saved in a json format by make_lexicon'''
    with open(filename, "r") as f:
        obj = json.load(f)
    lexicon = {literal_eval(k):v for k, v in obj.items()}
    return lexicon

def load_unigram(filename):
    '''loads a unigram_freq saved in a json format by make_lexicon'''
    with open(filename, "r") as f:
        unigram = json.load(f)
    return unigram

def get_freq(word_list, unigram):
    '''looks up the frequency of words, in a unigram frequency list
    Arguments: word_list - list of words to look up
    lexicon -- a loaded unigram
    Return none
    prints word, frequency pairs'''
    for i in word_list:
        if i in unigram:
            print(i+" "+str(unigram[i]))
        else:
            print(i+ " is not in the lexicon")

def check():
    distractor_dict=load_lexicon("lexicon.json")
    for key in distractor_dict:
        if len(distractor_dict[key])<100:
            print(str(key)+" : "+str(len(distractor_dict[key])))
    print(len(distractor_dict))
     
#check()
#parse_files()
#make_word_list()
#save_things()
