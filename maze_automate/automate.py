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
    if alts==None:
        print (word+" does not have alternates")
        return [word]
    else:
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
            for k in range(10):
                alt=random.choice(alts)
                if alt not in used_so_far:
                    alts_to_use.append(alt)
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
            f.write(" ".join(words[:(i+1)])+"\n\n") # context 
            f.write(" | "+words[i+1]+" | g: "+str(round(g_s[i][1][j]))+ " | 1_b: "+str(round(one_b_s[i][1][j]) + " |\n")
            f.write("|---|---|---|")
            for k in g_s[i][2][j]:
                f.write(" | "+k+ " | "+str(round(g_s[i][2][j][k]))+" | "+str(round(b_s_one[i][2][j][k]))+" |\n")
    f.close()

          
    
def process_sentences(sentences, filename):
    '''given sentence, file location, writes all sorts of useful stuff to file'''

    to_test=pre_surprisal(sentences)
    g_surprisal = g.Surprisal(to_test)
    one_b_surprisal = one_b.Surprisal(to_test)
    output(to_test, g_surprisal, one_b_surprisal, filename)

#test surprisal on some of their examples to get a baseline for how bad is bad

#and then see how much I need to try to get something that bad?

### deprecated
def do_sentence_badness(sentence, alts, filename):
    '''given sentence, alternate sentence, do stuff'''
    f=open(filename, "a")
    words=split_sentence(sentence)
    bad=split_sentence(alts)
    f.write(sentence+"  \n\n")
    f.write("|Freq \t| Google \t| Gulardova \t| Good \t| Alt \t| Freq \t| Google \t| Gulardova \t|\n")
    f.write("|---|---|---|---|---|---|---|---|\n")
    for i in range(1, len(words)):
        context=" ".join(words[:(i)])
        word=words[i]
        alt=bad[i]
        if word[-1] in [".",",","!", "?"]:
            word=word[:-1]
        if alt[-1] in [".",",", "!", "?"]:
            alt=alt[:-1]
        check_badness(context, word, alt, f)
    f.write("  \n")
    f.close()
def check_badness(context, word, alt,f):
    '''sees how much worse one word is than another given a context'''
    baseline_surp_b = get_surprisal(context, word)
    baseline_surp_g = get_surprisal(context, word, gulardova_surprisal)
    baseline_freq = get_unigram_freq(word)
    alt_surp_b = get_surprisal(context, alt)
    alt_surp_g= get_surprisal(context, alt, gulardova_surprisal)
    alt_freq = get_unigram_freq(alt)
    f.write("| "+str(round(baseline_freq))+"\t| "+str(round(baseline_surp_b))+"\t| "+str(round(baseline_surp_g))+"\t| "+word+"\t| "+alt+"\t| "+
        str(round(alt_freq))+"\t| "+str(round(alt_surp_b))+"\t| "+str(round(alt_surp_g))+"\t|\n")
        
def test_alternates(context, word, f):
    '''given context word, writes some stuff to the file'''
    f.write("\n"+context+"\n")
    alts =get_alternates(word)
    good=get_surprisal(context,word)
    good_2=get_surprisal(context,word, gulardova_surprisal)
    f.write("| "+word+"\t| Google: "+str(round(good))+"\t| Gulardova: "+str(round(good_2))+"|\n")
    f.write("|---|---|---|\n")
    used_so_far=[]
    for i in range(10):
        alt=random.choice(alts)
        if alt not in used_so_far:
            alt_surp_b=get_surprisal(context, alt)
            alt_surp_g=get_surprisal(context, alt, gulardova_surprisal)
            f.write("| "+alt+"\t| "+str(round(alt_surp_b))+"\t| "+str(round(alt_surp_g))+"|\n")
            used_so_far.append(alt)
    return
def check_lexicon():
    for key in sorted(LEXICON):
        print(key,"\t",len(LEXICON[key]))

### end deprecated
#do_sentence_badness("Yesterday the wife of the politician discussed health care with old people.", "x-x-x try when phrases for conclue plan hear city image I cute.", "output.txt")
process_sentences(["Yesterday the wife of the politician discussed health care with old people.","The children of the rich man were spoiled, but they were charming and handsome."], "output_new.txt")
#do_sentence_badness("The children of the rich man were spoiled, but they were charming and handsome.", "x-x-x of is were an same lawsuit reservation, unison door researchers are they atmosphere.", "output.txt")
do_sentence("The children of the rich man were spoiled, but they were charming and handsome.")
