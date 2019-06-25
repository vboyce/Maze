'''functions needed for both gulordava and one_b models'''

import random
import math
from wordfreq import zipf_frequency
import lexicon_generator_wf

LEXICON = lexicon_generator_wf.load_distractor_dict('distractor_list.json')

def get_unigram_freq(word):
    '''arguments: word - string
	returns unigram frequency '''
    raw_freq = zipf_frequency(word,'en') # use wordfreq to get log frequency
    freq=math.floor(math.log(10)*raw_freq) #rescale and floor to match a bin
    if freq>11:
        freq=11
    if freq<2:
        freq=2
    return freq

def strip_end_punct(word):
    '''take a word, return tuple of word without last end punctuation,
    if any, and end punctuation'''
    if word[-1] in [".", ",", "!", "?"]:
        return (word[:-1], word[-1])
    return(word, "")

def get_alts(length, freq):
    '''given two numbers (length, frequency), returns a list of words
    with that length and frequency'''
    if length < 4: #adjust length if needed
        length = 4
    if length > 15:
        length = 15
    alts = LEXICON.get((length, freq))
    if alts is None:
        print("Trouble finding words with length "+str(length)+ " and frequency "+str(freq))
    else:
        random.shuffle(alts)
    return alts

def get_alt_nums(word_list):
    ''' given a list of words, returns the average length and average frequency as a tuple'''
    length = 0
    freq = 0
    for i, _ in enumerate(word_list): #find individual length, freq
        word = strip_end_punct(word_list[i])[0]
        length += len(word)
        #print(type(freq))
        freq += get_unigram_freq(word)
    avg_length = round(length/len(word_list)) #take avg and round
    avg_freq = round(freq/len(word_list))
    return(avg_length, avg_freq)
    

