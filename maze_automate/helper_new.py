import random
import math
from wordfreq import zipf_frequency

which_freq = ""
LEXICON = {}
UNIGRAM_FREQ = {}

def specify(freq):
    global which_freq
    which_freq = freq
    if (freq == "wordfreq"):
        print("wordfreq")
        import lexicon_generator_wf
        LEXICON.update(lexicon_generator_wf.load_distractor_dict('distractor_list.json'))
    else:
        print("not wordfreq")
        import lexicon_generator
        UNIGRAM_TEMP = lexicon_generator.load_unigram('unigram.json')
        #make everything into lowercase so it is easier to find
        for word in UNIGRAM_TEMP:
            word_fix = word.lower()
            if (word_fix not in UNIGRAM_FREQ):
                UNIGRAM_FREQ[word_fix] = UNIGRAM_TEMP[word]
            else:
                UNIGRAM_FREQ[word_fix] += UNIGRAM_TEMP[word]
        LEXICON.update(lexicon_generator.load_lexicon('lexicon.json'))

def get_unigram_freq(word):
    '''arguments: word - string
	returns unigram frequency '''
    #using wordfreq
    if which_freq == "wordfreq":
        raw_freq = zipf_frequency(word,'en') # use wordfreq to get log frequency
        freq = math.floor(math.log(10)*raw_freq) #rescale and floor to match a bin
        freq = max(min(freq, 11), 2) #constrain freq within the range 2...11
        return freq
    #not using wordfreq
    word = word.lower()
    freq = UNIGRAM_FREQ.get(word)
    if freq is not None:
        return freq
    return 0 #word not found, hopefully is very rare

def strip_punct(word):
    '''take a word, return tuple of word without punctuations,
    if any, punctuation prefix, punctuation suffix, and word case'''
    prefix = ""
    suffix = ""
    for i in range(len(word)):
        if (word[i].isalnum()):
            break
    if (i > 0):
        prefix = word[:i]
    for j in range(len(word) - 1, 0, -1):
        if (word[j].isalnum()):
            break
    if (len(word) > 1 and j + 1 < len(word)):
        suffix = word[j+1:]
    elif (len(word) == 1):
        j = len(word) - 1
    word = word[i:j+1]
    if (word.isupper()):
        case = 2 #all capitalized
    elif (word[1].isupper()):
        case = 1 #first letter capitalized
    else:
        case = 0 #all lowercase
    return (word.lower(), prefix, suffix, case)

'''
def strip_end_punct(word):
    take a word, return tuple of word without last end punctuation,
    if any, and end punctuation
    if word[-1] in [".", ",", "!", "?"]:
        return (word[:-1], word[-1])
    return(word, "")
'''

min_length = 4 #changeable
max_length = 15
def get_alts(length, freq):
    '''given two numbers (length, frequency), returns a list of words
    with that length and frequency'''
    length = max(min(length, max_length), min_length)
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
    for raw_word in word_list: #find individual length, freq
        (word, _, _, _) = strip_punct(raw_word)
        length += len(word)
        freq += get_unigram_freq(word)
    avg_length = round(length/len(word_list)) #take avg and round
    avg_freq = round(freq/len(word_list))
    return (avg_length, avg_freq)
