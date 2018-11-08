import one_b_surprisal as one_b
import gulardova_surprisal as g
import lexicon_generator
import random
import re
import gulardova_suggest as g_suggest

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
    alts=[]
    i=0
    word_length=len(word)
    if word_length<3:
        word_length=3
    if word_length>15:
        word_length=15
    while len(alts)<50:
        a=LEXICON.get((word_length, get_unigram_freq(word)-1))
        if a!=None:
            alts.extend(a)
        i+=1
    if i>1:
        print("Trouble finding neighbors for "+word)
    return alts

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
                word=word[:-1]
            alts=get_alternates(word)
            alts_to_use=[]
            for i in range(50):
                if len(alts_to_use)>19:
                    break
                alt=random.choice(alts)
                if alt not in alts_to_use:
                    if alt==alt.lower():
                        alts_to_use.append(alt)
            list_of_alts.append(alts_to_use)
        to_surprisal.append((sentence,list_of_alts))
    return(to_surprisal)
    
def output(sentences, g_s, one_b_s, filename):
    f=open(filename, "a")
    for i in range(len(g_s)):
        f.write("\n\n"+sentences[i]+"\n\n")
        words=split_sentence(sentences[i])
        for j in range(len(words)-1):
            f.write(" ".join(words[:(j+1)])+"\n\n") # context 
            f.write("One b suggests: ")
            for l in range(len(one_b_s[i][3][j])):
                f.write("  "+one_b_s_[i][3][j][l])
            f.write("\nGulardova suggests: ")
            for l in range(len(g_s[i][3][j])):
                f.write("  "+one_b_s[i][3][j][l])
            f.write("\n\n | "+words[j+1]+" | g: "+str(int(round(g_s[i][1][j])))+ " | 1_b: "+str(int(round(one_b_s[i][1][j]))) + " |\n")
            f.write("|---|---|---|\n")
            for k in g_s[i][2][j]:
                f.write(" | "+k+ " | "+str(int(round(g_s[i][2][j][k])))+" | "+str(int(round(one_b_s[i][2][j][k])))+" |\n")
            f.write("\n")
    f.close()

def output_suggestions(g_results, filename):
    f=open(filename, "a")
    for i in range(len(g_results)):
        f.write("\n\n"+g_results[i][0]+"\n\n")
        words=split_sentence(g_results[i][0])
        for j in range(len(words)-1):
            f.write("\n\n"+" ".join(words[:(j+1)])+"\n\n") # context 
            for k in range(len(g_results[i][1][j])):
                f.write(" "+g_results[i][1][j][k])
    f.close()

def read_sentences(filename):
    f=open(filename, "r")
    sentences =[x.strip() for x in f.readlines()]
    f.close()
    return sentences
 
def process_sentences(in_file, out_file):
    '''given sentence, file location, writes all sorts of useful stuff to file'''
    sentences=read_sentences(in_file)
    to_test=pre_surprisal(sentences)
    g_surprisal = g.Surprisal(to_test)
    one_b_surprisal = one_b.Surprisal(to_test)
    output(sentences, g_surprisal, one_b_surprisal, out_file)

def get_suggestions(in_file, out_file):
    sentences=read_sentences(in_file)
    g_results=g_suggest.Suggest_Next(sentences)
    output_suggestions(g_results,out_file)

def check_lexicon():
    for key in sorted(LEXICON):
        print(key,"\t",len(LEXICON[key]))
process_sentences("input.txt", "output_5.md")
#get_suggestions("input.txt", "output_test.md")
#process_sentences("intest.txt", "outtest.md")
#check_lexicon()

