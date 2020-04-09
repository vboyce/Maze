import logging
from nltk.tokenize import word_tokenize
def strip_punct(word):
    '''take a word, return word with start and end punctuation removed'''
    for i in range(len(word)):
        if word[i].isalnum():
            break
    for j in range(len(word) - 1, -1, -1):
        if word[j].isalnum():
            break
    word = word[i:j + 1]
    return word

def copy_punct(word,distractor):
    """Takes the start and end punctuation of word as well as the capitalization pattern
    and return distractor with that punctuation and capitalization"""
    for i in range(len(word)):
        if word[i].isalnum():
            break
    prefix=word[0:i]
    for j in range(len(word) - 1, -1, -1):
        if word[j].isalnum():
            break
    suffix=word[j+1:]
    word = word[i:j + 1]
    if len(word) > 1 and word.isupper():
        distractor=distractor.upper()  # all capitalized
    elif len(word) > 1 and word[0].isupper():
        distractor=distractor[0:1].upper()+distractor[1:]  # first letter capitalized
    else:
        distractor=distractor.lower()  # all lowercase
    distractor=prefix+distractor+suffix
    return distractor

def tokenize(word):
    """because someone needs to pull off those initial single quotes"""
    tokens=[]
    end_tokens=[]
    for i in range(len(word)):
        if word[i].isalnum():
            break
        else:
            tokens.append(word[i])
    for j in range(len(word) - 1, -1, -1):
        if word[j].isalnum():
            break
        else:
            end_tokens.append(word[j])
    end_tokens.reverse()
    word = word[i:j + 1]
    word_tokens=word_tokenize(word)
    tokens.extend(word_tokens)
    tokens.extend(end_tokens)
    return tokens