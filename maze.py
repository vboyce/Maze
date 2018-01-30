import numpy

x=["The dog went to the park.", "Look, a rainbow!"]

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
            new_words.append(redo_case("".join(new), case, punc))
        if dashed:
            nonsense="--- "+" ".join(new_words[1:])
        else:
            nonsense=" ".join(nonce)
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
    alphabet="abcdefghijklmnoqrstuvwxyz"
    return (numpy.random.choice(list(alphabet), (len(word))))

def anagram(word):
    '''takes a string and returns an anagram, guaranteed to not be the same as the starting word
    exception: for one letter words, returns some random one letter word'''
    if len(word)==1:
        return nonce(word)
    else:
        nagaram=list(word)
        while (numpy.array_equiv(nagaram, list(word))):
            nagaram=numpy.random.choice(list(word), len(word), replace=False)
        return nagaram

def ibex_format(item_name, sentences, distractors, file=None):
    '''given a list of item names, a list of sentences and a list of distrator items, produces a string suitable
for including in the items list of an ibex experiment. If a file is given, writes to there as well.'''
    if not len(item_name)==len(sentences):
        raise Exception("item_name and sentences are not same length")
    if not len(sentences)==len(distractors):
        raise Exception("sentences and distractors are not the same length")
    items=""
    for i in range(len(sentences)):
        items+=("[\""+item_name[i]+"\", \"Maze\", {s: \""+sentences[i]+"\", a: \""+distractors[i]+"\"}],\n")
    if file:
        f=open(file, "w")
        f.writelines(items)
    return items
                   
#ibex_format(["test", "test"], x, distractor(x, dashed=True))



