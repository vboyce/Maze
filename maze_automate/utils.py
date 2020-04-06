import logging

def strip_punct(word):
    '''take a word, return word with start and end punctuation removed'''
    for i in range(len(word)):
        if word[i].isalnum():
            break
    for j in range(len(word) - 1, 0, -1):
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
    for j in range(len(word) - 1, 0, -1):
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

