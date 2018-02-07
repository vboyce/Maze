import numpy
import csv
import sys

###Settings:###
# Set these to specify what options you want#
#options for mode are "nonce" and "anagram"
mode="anagram"
#options for dashes are False and True
dashes=True
#specify a file name for the output
output_file="ibex-master/data_includes/ibex_data.js"
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


#define global variables WORDLIST and ALPHABET
with open("celex_words.txt") as celex:
    words=celex.readlines()
words=[x.strip().lower() for x in words]
WORDLIST=set(words)
ALPHABET="abcdefghijklmnoqrstuvwxyz"


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
    mode can be nonce or anagram'''
    output=[]
    for i in range(len(data)):
        words=data[i].split(" ")
        new_words=[]
        for i in range(len(words)):
            lower,case, punc=undo_case(words[i])
            if mode=="nonce":
                new=nonce(lower)
            if mode=="anagram":
                new=anagram(lower)
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

def nonce(word):
    '''takes a string and returns length matched string of random letters; output guaranteed not in celex list
    for words of length 2+; for single letter, returns a letter that is not a,i,o
    '''
    if len(word)==1:
        return(single_letter())
    while True:
        test="".join(numpy.random.choice(list(ALPHABET), (len(word))))
        if test not in WORDLIST:
            return test


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
    '''given a list of item names, a list of sentences and a list of distrator items, a header, and a footer, produces a string suitable
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
    filename=sys.argv[1]
    sentences, items=read_input(filename)
    distractors=distractor(sentences, mode, dashes)
    ibex_format(items, sentences, distractors, header, footer, output_file)
