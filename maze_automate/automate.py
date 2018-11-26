# Copyright (c) 2018-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import torch
import torch.nn as nn
import torch.nn.functional as F
from nltk.tokenize import word_tokenize
from gulardova_code import dictionary_corpus
from gulardova_code.utils import repackage_hidden, batchify, get_batch
import numpy as np
import lexicon_generator
import random
import re
import csv
import os
import sys

import numpy as np
from six.moves import xrange
import tensorflow as tf
from nltk.tokenize import word_tokenize
from google.protobuf import text_format
from one_b_code import data_utils
#### General functions ####
UNIGRAM_FREQ=lexicon_generator.load_unigram('unigram.json')
LEXICON=lexicon_generator.load_lexicon('lexicon.json')

def get_unigram_freq(word):
    '''takes word, returns unigram frequency'''
    freq=UNIGRAM_FREQ.get(word)
    #print(type(freq))
    if freq!=None:
        return freq
    else:
        print (word+" is not in dictionary")

def strip_end_punct(word):
    if word[-1] in [".",",","!", "?"]:
        return (word[:-1],word[-1])
    return(word, "")

def get_alts(length, freq):
    '''given a list of words, returns candidate buddies
    buddies = match the average length, frequency bin of word list'''
    if length<3: #adjust length if needed
        length=3
    if length>15:
        length=15
    alts=LEXICON.get((length, freq))
    if alts==None:
        print("Trouble finding neighbors for "+" ".join(word_list))
    else:
        random.shuffle(alts)
    return alts

def get_alt_nums(word_list):
    length=0
    freq=0
    for w in range(len(word_list)): #find individual length, freq
        word=strip_end_punct(word_list[w])[0]
        length+=len(word)
        #print(type(freq))
        freq+=get_unigram_freq(word)
    avg_length=round(length/len(word_list)) #take avg and round
    avg_freq=round(freq/len(word_list))
    return(avg_length, avg_freq)

def save_output(outfile,item_to_info, end_result):
    with open(outfile, 'w') as f:
        for key in item_to_info:
            for i in range(len(item_to_info[key][1])):
                f.write('"'+item_to_info[key][0][i]+'";')
                f.write('"'+key+'";')
                f.write('"'+item_to_info[key][1][i]+'";')
                f.write('"'+end_result[item_to_info[key][1][i]]+'"\n')

def read_input(filename):
    '''file should be csv format with first column "tag" (any info that should stay associated with the sentence such as condition etc (it will be copied to eventual output), item number (sentences that share item num will get same distractors, and *Must* have same # of words, and sentence'''
    item_to_info={}
    with open(filename, 'r') as tsv:
        f = csv.reader(tsv, delimiter=";", quotechar='"')
        for row in f:
            if row[1] in item_to_info:
                item_to_info[row[1]][0].append(row[0])
                item_to_info[row[1]][1].append(row[2])
            else:
                item_to_info[row[1]]=[[row[0]],[row[2]]]
    sentences=[]
    for item in sorted(item_to_info):
        sentences.append(item_to_info[item][1])
    return (item_to_info, sentences)

def mainish(infile, outfile, lang_model="gula"):
    item_to_info, sentences=read_input(infile)
    end_result={}
    if lang_model=="gula":
        model, device =load_model_gula()
        dictionary, ntokens = load_dict_gula()
        for i in range(len(sentences)):
            bad=do_sentence_set_gula(sentences[i], model, device, dictionary, ntokens)
            for j in range(len(sentences[i])):
                end_result[sentences[i][j]]=bad
    elif lang_model=="one_b":
        sess, t =load_model_one_b()
        vocab=load_dict_one_b()
        for i in range(len(sentences)):
            bad=do_sentence_set_one_b(sentences[i],sess, t, vocab)
            for j in range(len(sentences[i])):
                end_result[sentences[i][j]]=bad
    save_output(outfile,item_to_info, end_result)


def check_lexicon():
    for key in sorted(LEXICON):
        if key[0]==3:
            for i in LEXICON[key]:
                print(i)

#### Gulardova specific ####
def load_model_gula():
    with open("gulardova_data/hidden650_batch128_dropout0.2_lr20.0.pt", 'rb') as f:
        print("Loading the model")
        # to convert model trained on cuda to cpu model
        model = torch.load(f, map_location = lambda storage, loc: storage) #read the serialized model into an object
    model.eval() #put model in eval mode
    model.cpu() # put it on cpu 
    device = torch.device("cpu") #what sort of data model is stored on
    return (model, device)

def load_dict_gula():
    dictionary = dictionary_corpus.Dictionary("gulardova_data") #load a dictionary
    ntokens = dictionary.__len__() #length of dictionary
    return(dictionary, ntokens)

def new_sentence_gula(model, device, ntokens):
    hidden = model.init_hidden(1) #sets initial values on hidden layer 
    input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device) #gets a random wordid from vocab list
    return (input, hidden)

def update_sentence_gula(word, input, model, hidden, dictionary):
    parts=word_tokenize(word) #get list of tokens
    for part in parts:
       token = dictionary_corpus.tokenize_str(dictionary,part)[0] #get id of token
       if part not in dictionary.word2idx:
            print("Good word "+part+" is unknown") #error message
       input.fill_(token.item()) #fill with value of token
       output, hidden = model(input,hidden) #do the model thing       
       word_weights = output.squeeze().div(1.0).exp().cpu() #process output into weights
       word_surprisals = -1*torch.log2(word_weights/sum(word_weights))# turn into surprisals
    return (output, hidden, word_surprisals)

def get_surprisal_gula(surprisals, dictionary, word):
    token=dictionary_corpus.tokenize_str(dictionary, word)[0] #take first token of word
    if word not in dictionary.word2idx:
        print(word+" is unknown")
        return(-1) #use -1 as an error code
    else:
        return surprisals[token].item() #numeric value of word's surprisal

def find_bad_enough_gula(num_to_test, minimum, word_list, surprisals_list, dictionary):
    '''will return the word that is at least minimum surprisal for all sentences. if goes through num_to_test words
    without finding a bad enough, returns the worst it's seen (worst= highest min)
    pass
    options_list = list of words that can be tested
    surprisals_list = list of surprisal distributions'''    
    best_word=""
    best_surprisal=0
    length, freq=get_alt_nums(word_list)
    options_list=None
    i=0
    k=0
    while options_list==None:
        options_list=get_alts(length, freq+i)
        i+=1
    while best_surprisal==0 or k<num_to_test:
        min_surprisal=100
        if k==len(options_list):
            new_options=None
            while new_options==None:
                new_options=get_alts(length, freq+i)
                i+=1
            options_list.extend(new_options)
        word=options_list[k]
        k+=1
        for j in range(len(surprisals_list)):
            surprisal=get_surprisal_gula(surprisals_list[j], dictionary, word)
            min_surprisal=min(min_surprisal, surprisal)
            if min_surprisal>=minimum:
                return (word)
            elif min_surprisal>best_surprisal:
                best_word=word
                best_surprisal=min_surprisal
    print("Couldn't meet surprisal target, returning with surprisal of "+str(best_surprisal))
    return(best_word)
            

def do_sentence_set_gula(sentence_set, model, device, dictionary, ntokens):
    bad_words=["x-x-x"]
    words=[]
    sentence_length=len(sentence_set[0].split())
    for i in range(len(sentence_set)):
        sentence=sentence_set[i] 
        sent_words=sentence.split()
        if len(sent_words)!=sentence_length:
            print("inconsistent lengths!!")  
        words.append(sent_words)
    hidden=[None]*len(sentence_set)
    input=[None]*len(sentence_set)
    output=[None]*len(sentence_set)
    surprisals=[None]*len(sentence_set)
    for i in range(len(sentence_set)):
        input[i], hidden[i]=new_sentence_gula(model, device, ntokens)
    for j in range(sentence_length-1):
        word_list=[]
        for i in range(len(sentence_set)):
            output[i], hidden[i], surprisals[i] = update_sentence_gula(words[i][j], input[i], model, hidden[i], dictionary)
            word_list.append(words[i][j+1])
        bad_word=find_bad_enough_gula(100, 23, word_list, surprisals, dictionary)
        cap=word_list[0][0].isupper()
        if cap:
            bad_word=bad_word[0].upper()+bad_word[1:]
        bad_word=bad_word+strip_end_punct(word_list[0])[1]
        bad_words.append(bad_word)
    bad_sentence=" ".join(bad_words)
    return(bad_sentence)

#### One b specific ####
def load_model_one_b():
    """Load the model from GraphDef and Checkpoint.
    TensorFlow session and tensors dict.
    """
    with tf.Graph().as_default():
    
        with tf.gfile.FastGFile("one_b_data/graph-2016-09-10.pbtxt", 'r') as f:
            s = f.read()
            gd = tf.GraphDef()
            text_format.Merge(s, gd)

        tf.logging.info('Recovering Graph %s', "one_b_data/graph-2016-09-10.pbtxt")
        t = {}
        [t['states_init'], t['lstm/lstm_0/control_dependency'],
         t['lstm/lstm_1/control_dependency'], t['softmax_out'], t['class_ids_out'],
         t['class_weights_out'], t['log_perplexity_out'], t['inputs_in'],
         t['targets_in'], t['target_weights_in'], t['char_inputs_in'],
         t['all_embs'], t['softmax_weights'], t['global_step']
        ] = tf.import_graph_def(gd, {}, ['states_init',
                                         'lstm/lstm_0/control_dependency:0',
                                         'lstm/lstm_1/control_dependency:0',
                                         'softmax_out:0',
                                         'class_ids_out:0',
                                         'class_weights_out:0',
                                         'log_perplexity_out:0',
                                         'inputs_in:0',
                                         'targets_in:0',
                                         'target_weights_in:0',
                                         'char_inputs_in:0',
                                         'all_embs_out:0',
                                         'Reshape_3:0',
                                         'global_step:0'], name='')

        sys.stderr.write('Recovering checkpoint %s\n' % "one_b_data/ckpt-*")
        sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
        sess.run('save/restore_all', {'save/Const:0': "one_b_data/ckpt-*"})
        sess.run(t['states_init'])
    return (sess, t)            

def load_dict_one_b():
    vocab=data_utils.CharsVocabulary("one_b_data/vocab-2016-09-10.txt", 50)
    return(vocab)

def new_sentence_one_b(vocab):
    targets = np.zeros([1, 1], np.int32)
    weights = np.ones([1, 1], np.float32)
    inputs = np.zeros([1, 1], np.int32)
    char_ids_inputs = np.zeros( [1, 1, vocab.max_word_length], np.int32)
    return (targets, weights, inputs, char_ids_inputs)       

def tokenize_one_b(word):
    new_string=re.sub("([.,?!])", r" \1 ", word)
    newer_string=re.sub("'", " '", new_string)
    tokens=newer_string.split()
    return tokens
    
def update_sentence_one_b(word, inputs, char_ids_inputs, sess, t, targets, weights, vocab):
    parts=tokenize_one_b(word) #get list of tokens
    for part in parts:
        token = vocab.word_to_id(part)#get id of token
        char_tokens=vocab.word_to_char_ids(part) #get char ids
        if token==vocab.unk:
            print("Good word "+part+" is unknown") #error message
        inputs[0,0]=token
        char_ids_inputs[0,0,:]=char_tokens
        softmax = sess.run(t['softmax_out'],
                                     feed_dict={t['char_inputs_in']: char_ids_inputs,
                                                t['inputs_in']: inputs,
                                                t['targets_in']: targets,
                                                t['target_weights_in']: weights})
    return (targets, weights, softmax)

def get_surprisal_one_b(softmax, vocab, word):
    token=vocab.word_to_id(word) #take first token of word
    if token ==vocab.unk:
        print(word+" is unknown")
        return(-1) #use -1 as an error code
    else:
        return -1 * np.log2(softmax[0][token]) #numeric value of word's surprisal

def find_bad_enough_one_b(num_to_test, minimum, word_list, surprisals_list, vocab):
    '''will return the word that is at least minimum surprisal for all sentences. if goes through num_to_test words
    without finding a bad enough, returns the worst it's seen (worst= highest min)
    pass
    options_list = list of words that can be tested
    surprisals_list = list of surprisal distributions'''    
    best_word=""
    best_surprisal=0
    length, freq=get_alt_nums(word_list)
    options_list=None
    i=0
    k=0
    while options_list==None:
        options_list=get_alts(length, freq+i)
        i+=1
    while best_surprisal==0 or k<num_to_test:
        min_surprisal=100
        if k==len(options_list):
            new_options=None
            while new_options==None:
                new_options=get_alts(length, freq+i)
                i+=1
            options_list.extend(new_options)
        word=options_list[k]
        k+=1
        for j in range(len(surprisals_list)):
            surprisal=get_surprisal_one_b(surprisals_list[j], vocab, word)
            min_surprisal=min(min_surprisal, surprisal)
            if min_surprisal>=minimum:
                return (word)
            elif min_surprisal>best_surprisal:
                best_word=word
                best_surprisal=min_surprisal
    print("Couldn't meet surprisal target, returning with surprisal of "+str(best_surprisal))
    return(best_word)

def do_sentence_set_one_b(sentence_set, sess, t, vocab):
    bad_words=["x-x-x"]
    words=[]
    sentence_length=len(sentence_set[0].split())
    for i in range(len(sentence_set)):
        sentence=sentence_set[i] 
        sent_words=sentence.split()
        if len(sent_words)!=sentence_length:
            print("inconsistent lengths!!")  
        words.append(sent_words)
    inputs=[None]*len(sentence_set)
    char_ids_inputs=[None]*len(sentence_set)
    weights=[None]*len(sentence_set)
    targets=[None]*len(sentence_set)
    softmaxes=[None]*len(sentence_set)
    for i in range(len(sentence_set)):
        targets[i], weights[i], inputs[i], char_ids_inputs[i]=new_sentence_one_b(vocab)
    for j in range(sentence_length-1):
        word_list=[]
        for i in range(len(sentence_set)):
            targets[i], weights[i], softmaxes[i] = update_sentence_one_b(words[i][j], inputs[i], char_ids_inputs[i], sess, t, targets[i], weights[i], vocab)
            word_list.append(words[i][j+1])
        bad_word=find_bad_enough_one_b(100, 23, word_list, softmaxes, vocab)
        cap=word_list[0][0].isupper()
        if cap:
            bad_word=bad_word[0].upper()+bad_word[1:]
        bad_word=bad_word+strip_end_punct(word_list[0])[1]
        bad_words.append(bad_word)
    bad_sentence=" ".join(bad_words)
    return(bad_sentence)
#####
mainish("test_input.txt", "output2.txt", "one_b")   
mainish("test_input.txt", "output1.txt", "gula")
#print(type(get_unigram_freq("can't")))
#check_lexicon()
#print(get_unigram_freq("won't"))
#print(get_unigram_freq("isn't"))
#print(get_unigram_freq("is"))
#print(get_unigram_freq("can't"))
#print(get_unigram_freq("will"))
#print(get_unigram_freq("bird"))
#print(get_unigram_freq("neonate"))
#print(get_unigram_freq("dribble"))
#print(tokenize_one_b("can't."))
