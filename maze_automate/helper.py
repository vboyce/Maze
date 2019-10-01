'''functions needed for both gulordava and one_b models'''

import random

import lexicon_generator

UNIGRAM_FREQ = lexicon_generator.load_unigram('unigram.json')
LEXICON = lexicon_generator.load_lexicon('lexicon.json')

def get_unigram_freq(word):
    '''arguments: word - string
	returns unigram frequency '''
    freq = UNIGRAM_FREQ.get(word)
    if freq is not None:
        return freq
    #try different capitalization schemes
    print(word+" is not in dictionary")
    test_freq = UNIGRAM_FREQ.get(word.lower())
    if test_freq is not None:
        print("Using "+word.lower()+" instead")
        return test_freq
    test_freq = UNIGRAM_FREQ.get(word.capitalize())
    if test_freq is not None:
        print("Using "+word.capitalize()+" instead")
        return test_freq
    return None

def strip_end_punct(word):
    '''take a word, return tuple of word without last end punctuation,
    if any, and end punctuation'''
    if word[-1] in [".", ",", "!", "?"]:
        return (word[:-1], word[-1])
    return(word, "")

def get_alts(length, freq):
    '''given two numbers (length, frequency), returns a list of words
    with that length and frequency'''
    if length < 3: #adjust length if needed
        length = 3
    if length > 15:
        length = 15
    alts = LEXICON.get((length, freq))
    if alts is None:
        print("Trouble finding words with length "+str(length)+ " and frequency "+str(freq))
        alts = []
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
