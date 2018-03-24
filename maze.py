import numpy
import csv
import sys
import argparse

#defaults 
#what ibex stuff goes at the top of the file
header=('var shuffleSequence = seq("intro",followEachWith("sep","test"), "done");\n\n'
    'var showProgressBar =false;\n\n'
    'var items = [\n\n'
    '\t["intro", "Message", {html: "This is a demo of the maze task implemented in ibex.'
    ' You will read a sentence word by word. On each screen you will see two words, one of'
    ' which is a reasonable continuation of the sentence. Use your left and right arrow '
    'buttons to indicate which word is the correct continuation. The sentence will start with \'the\'." }],'
    '\n\t["sep", "MazeSeparator", {normalMessage: "Correct! Press any key to continue",'
    ' errorMessage: "Incorrect! Press any key to continue."}],'
    '\n\t["done", "Message", {html: "All done!"}]')
#what ibex stuff goes towards the end of the file
footer=('\n];')


#define global variables WORDLIST, ALPHABET, and NONCELIST
with open("celex_words.txt") as celex:
    words=celex.readlines()
words=[x.strip().lower() for x in words]
WORDLIST=set(words)
ALPHABET="abcdefghijklmnoqrstuvwxyz"

#a list of lists of noncewords by length (generated from Wuggy run on Wuggy's orthographic english list,
#with defaults except 1 nonce/real word and no more than 1 second to find a nonce for each real word
#guaranteed not in celex word list
NONCELIST=[[] for _ in range(30)]
with open("noncewords.txt") as nonce_list:
    nonce_list=csv.reader(nonce_list, delimiter='\t')
    next(nonce_list)
    for row in nonce_list:
        word=str(row[1])
        if word not in NONCELIST[len(word)]:
            if word not in WORDLIST:
                NONCELIST[len(word)].append(word)

def read_input(file):
    '''file: location/name of a tsv file with input sentences in column 1 and and item labels in column 2
    returns a tuple of lists;first is list of sentences, second is list of item labels'''
    sentences=[]
    items=[]
    with open(file) as f:
        line=csv.reader(f, delimiter='\t')
        for row in line:
            sentences.append((row[0]))
            items.append((row[1]))
    return (sentences, items)

def distractor(data, mode="nonce", dashed=False):
    '''Given a list of sentences, returns a same size list of distractor word sentences.
    If dashed=True, first word of each fake sentence is set to be ---
    mode can be nonce, good_nonce or anagram'''
    output=[]
    for i in range(len(data)):
        words=data[i].split(" ")
        new_words=[]
        for i in range(len(words)):
            lower,case, punc=undo_case(words[i])
            if mode=="gibber":
                new=gibber(lower)
            if mode=="anagram":
                new=anagram(lower)
            if mode=="nonce":
                new=nonce(lower)
            new_words.append(redo_case(new, case, punc))
        if dashed:
            nonsense="--- "+" ".join(new_words[1:])
        else:
            nonsense=" ".join(new_words)
        output.append(nonsense)
    return(output)

def undo_case(word):
    '''returns tuple of lower case word, boolean for whether it was capitilized, and string of end punctuation'''
    suffix=""
    iscap=word[0].isupper()
    if not word[-1].isalpha():
        suffix=word[-1]
        word=word[:-1]
    return ((word.lower(), iscap, suffix))

def redo_case(word, case, punc):
    '''takes in lower case word and boolean for whether it should be capitilized,
    returns word'''
    if case:
        return(word[0].upper()+word[1:]+punc)
    else:
        return(word+punc)

def gibber(word):
    '''takes a string and returns length matched string of random letters; output guaranteed not in celex list
    for words of length 2+; for single letter, returns a letter that is not a,i,o
    '''
    if len(word)==1:
        return(single_letter())
    while True:
        test="".join(numpy.random.choice(list(ALPHABET), (len(word))))
        if test not in WORDLIST:
            return test

def nonce(word):
    '''takes a string and returns length matched orthographically legal non word; output guaranteed not
    in celex list for words of length 2+; for single letter, returns a letter that is not a,i,o
    non words sourced from Wuggy'''
    if len(word)==1:
        return(single_letter())
    while True:
        test=numpy.random.choice(NONCELIST[len(word)])
        return(test)

def anagram(word):
    '''takes a string and returns an anagram; output guaranteed not in celex list;
    if first 10 attempts to find non-word anagram fails, replaces the first letter
    with a random letter and tries again
    for words of length one returns a letter that is not a,i,o '''
    
    if len(word)==1:
        return(single_letter())
    for i in range(10):
        nagaram="".join(numpy.random.choice(list(word), len(word), replace=False))
        if nagaram not in WORDLIST:
            return nagaram
    print("Warning, can't find valid angram of "+word)
    new_word="".join(numpy.random.choice(list(ALPHABET), 1))+word[1:]
    return(anagram(new_word))

def single_letter():
    '''returns a letter that is not a,i,o; all single letters are in celex, but other than these three
    they aren't really words'''
    safe_single_letter="bcdefghjklmnpqrstuvwxyz" #ommitting a,i,o on the basis of being ~words
    test="".join(numpy.random.choice(list(safe_single_letter), 1))
    return test                                      

def ibex_format(item_name, sentences, distractors,header, footer, file=None, ):
    '''given a list of item names, a list of sentences and a list of distrator items,
    a header, and a footer, produces a string suitable
    for running in ibex. If a file is given, writes to there as well.'''
    if not len(item_name)==len(sentences):
        raise Exception("item_name and sentences are not same length")
    if not len(sentences)==len(distractors):
        raise Exception("sentences and distractors are not the same length")
    items=header
    for i in range(len(sentences)):
        items+=(",\n\t[\""+item_name[i]+"\", \"Maze\", {s: \""+sentences[i]+"\", a: \""+distractors[i]+"\"}]")
    items+=footer
    if file:
        f=open(file, "w")
        f.writelines(items)
    return items

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Take materials and output an ibex maze data file')
    parser.add_argument('filename', metavar='Input', type=str, help='file with input in tsv format,'+
                        'first column sentences, second column item labels')
    parser.add_argument('write_to', metavar='Output', type=str, help='file to write output to')
    parser.add_argument('--top','-t', type=str, help='use contents of this file instead of default header')
    parser.add_argument('--bottom','-b', type=str, help='use contents of this file instead of default footer')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--anagram', '-a', dest='mode', action='store_const',const='anagram', default='nonce',
                        help='use anagrams as distractors')
    modes.add_argument('--gibber', '-g', dest='mode', action='store_const',const='gibber', default='nonce',
                        help='use random letter sequences as distractors')
    modes.add_argument('--nonce', '-n', dest='mode', action='store_const', const='nonce',
                        default='nonce', help='use orthographically legal nonwords as distractors (default)')
    dashes = parser.add_mutually_exclusive_group()
    dashes.add_argument('--allword', '-w', dest='dashes', action='store_const', const=False, default=True,
                        help='use a normal distractor for the first pair')
    dashes.add_argument('--firstdash', '-d', dest='dashes', action='store_const', const=True, default=True,
                        help='use --- as the first distractor (default)')
    args=vars(parser.parse_args())
    if args['top']:
        with open(args['top']) as f:
            header=f.read()
    if args['bottom']:
        with open(args['bottom']) as f:
            footer=f.read()
    sentences, items=read_input(args['filename'])
    distractors=distractor(sentences, args['mode'], args['dashes'])
    ibex_format(items, sentences, distractors, header, footer, args['write_to'])
