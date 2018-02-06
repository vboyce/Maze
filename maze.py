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
    '''given a file name/path, reads in contents of file into two line by line list.'''
    sentences=[]
    items=[]
    with open(file) as f:
        line=csv.reader(f, delimiter='\t')
        for row in line:
            sentences.append((row[0]))
            items.append((row[1]))
    return (sentences, items)

def distractor(data, mode="nonce", dashed=False):
    '''Given an array of sentences, returns a same size array of distractor word sentences.
    If dashed=True, first word of each fake sentence is set to be ---
    mode can be nonce or anagram
    if mode is nonce, distractor sentence have same word length as original, but random letters
    if mode is anagram, distractor sentence is word by word anagram of original, with exception if length 1 words'''
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
    '''returns string of random letters of length word'''
    for i in range(10):
        test="".join(numpy.random.choice(list(ALPHABET), (len(word))))
        if test not in WORDLIST:
            return test
    return(nonce(word+"a"))

def anagram(word):
    '''takes a string and returns an anagram '''
    for i in range(10):
        nagaram="".join(numpy.random.choice(list(word), len(word), replace=False))
        if nagaram not in WORDLIST:
            return nagaram
    print("Warning, can't find valid angram of "+word)
    new_word="".join(numpy.random.choice(list(ALPHABET), 1))+word
    return(anagram(new_word))

def ibex_format(item_name, sentences, distractors,header, footer, file=None, ):
    '''given a list of item names, a list of sentences and a list of distrator items, produces a string suitable
for including in the items list of an ibex experiment. If a file is given, writes to there as well.'''
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
