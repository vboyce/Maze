import one_b_surprisal as one_b
import gulardova_surprisal as g
import lexicon_generator
import random
import re

#Semiuseful notes:
#probably should use normal case for surprisal
#will need to deal with reparsing punctuation for everything at some point

UNIGRAM_FREQ=lexicon_generator.load_unigram('unigram.json')
LEXICON=lexicon_generator.load_lexicon('lexicon.json')

def get_unigram_freq(word):
    '''takes word, returns unigram frequency'''
    freq=UNIGRAM_FREQ.get(word)
    if freq!=None:
        return freq
    else:
        print (word+" is not in dictionary")

def get_alternates(word):
    '''given a word, returns candidate buddies'''
    alts=LEXICON.get((len(word),get_unigram_freq(word)))
    if len(alts)>50: #have enough options
        return alts
    else: #not enough options, opt for slightly less frequent
        alts.extend(LEXICON.get((len(word), get_unigram_freq(word)-1))
        if len(alts)>50:
            print ("Not enough neighbors for "+word)
            return alts
        else:
            print("Really not enough neighbors for "+word)
            return alts.append(word)
        

def split_sentence(sentence):
    '''takes sentence, returns list of word-units. one day might do parsing with punctuation'''
    return sentence.split()

def pre_surprisal(sentences):
    to_surprisal=[]
    for j in range(len(sentences)):
        sentence=sentences[j]
        words=split_sentence(sentence)
        list_of_alts=[]
        for i in range(1, len(words)):
            word=words[i]
            if word[-1] in [".",",","!", "?"]:
                punct=word[-1]
                word=word[:-1]
            else:
                punct=""
            alts=get_alternates(word)
            alts_to_use=[]
            while len(alts_to_use)<20:
                alt=random.choice(alts)
                if alt not in alts_to_use:
                    if alt==alt.lower():
                        alts_to_use.append(alt+punct)
            list_of_alts.append(alts_to_use)
        to_surprisal.append((sentence,list_of_alts))
    return(to_surprisal)
    
def output(sentences, g_s, one_b_s, filename):
    f=open(filename, "a")
    for i in range(len(g_s)):
        f.write("\n\n"+sentences[i]+"\n")
        f.write("\n"+g_s[i][0]+"\n")
        f.write("\n"+one_b_s[i][0]+"\n\n")
        words=split_sentence(sentences[i])
        for j in range(len(g_s[i][1])):
            f.write(" ".join(words[:(j+1)])+"\n\n") # context 
            f.write(" | "+words[j+1]+" | g: "+str(round(g_s[i][1][j]))+ " | 1_b: "+str(round(one_b_s[i][1][j])) + " |\n")
            f.write("|---|---|---|\n")
            for k in g_s[i][2][j]:
                f.write(" | "+k+ " | "+str(round(g_s[i][2][j][k]))+" | "+str(round(one_b_s[i][2][j][k]))+" |\n")
            f.write("\n")
    f.close()

def read_sentences(filename):
    f=open(filename, "r")
    sentences =[x.strip for x in f.readlines()]
    f.close()
    return sentences
 
def process_sentences(in_file, out_filename):
    '''given sentence, file location, writes all sorts of useful stuff to file'''
    sentences=read_sentences(in_file)
    to_test=pre_surprisal(sentences)
    g_surprisal = g.Surprisal(to_test)
    one_b_surprisal = one_b.Surprisal(to_test)
    output(sentences, g_surprisal, one_b_surprisal, filename)

def check_lexicon():
    for key in sorted(LEXICON):
        print(key,"\t",len(LEXICON[key]))

### end deprecated
process_sentences("input.txt", "output_4.md")
