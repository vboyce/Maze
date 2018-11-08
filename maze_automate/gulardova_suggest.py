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


def Suggest_Next(sentence_input):
    '''returns the surprisal of the last word, given the rest as context'''
    # Set the random seed manually for reproducibility.
    torch.manual_seed(1111)

    with open("gulardova_data/hidden650_batch128_dropout0.2_lr20.0.pt", 'rb') as f:
        print("Loading the model")
        # to convert model trained on cuda to cpu model
        model = torch.load(f, map_location = lambda storage, loc: storage)
    model.eval()

    model.cpu()

    #print("#####HERE###")
        
    eval_batch_size = 1
    seq_len = 20

    dictionary = dictionary_corpus.Dictionary("gulardova_data")
    vocab_size = len(dictionary)
    #print("Vocab size", vocab_size)
    #print("TESTING")

    # assuming the mask file contains one number per line indicating the index of the target word
    index_col = 0

    ntokens = dictionary.__len__()
    device = torch.device("cpu")
    ###
    result=[]
    for j in range(len(sentence_input)):
        print("Gulardova "+str(j))
        sentence=sentence_input[j]
        
        torch.manual_seed(1111)
        hidden = model.init_hidden(1)
        input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device)
        
        good_words=sentence.split()
        good_tokens=[word_tokenize(x) for x in good_words]
        firstword = dictionary_corpus.tokenize_str(dictionary,good_tokens[0][0])[0]
        if good_tokens[0][0] not in dictionary.word2idx:
            print("Good word "+good_tokens[0][0]+" in unknown")
        input.fill_(firstword.item())
        output, hidden = model(input,hidden)
        
        for j in range(1, len(good_tokens[0])): 
            next_token=dictionary_corpus.tokenize_str(dictionary,good_tokens[0][j])[0]
            if good_tokens[0][j] not in dictionary.word2idx:
                print("Good word "+good_tokens[0][j]+" is unknown")
            input.fill_(next_token.item())
            output, hidden = model(input, hidden)
            
        results_list=[]
        for i in range(len(good_words)-1):
            results=[]
            for k in range(5):
                word_weights = output.squeeze().div(1.0).exp().cpu()
                suggest_token=torch.multinomial(word_weights, 1)[0]
                results.append(dictionary.idx2word[suggest_token])
            good_word=dictionary_corpus.tokenize_str(dictionary,good_tokens[i+1][0])[0]
            if good_tokens[i+1][0] not in dictionary.word2idx:
                print("Good word "+good_tokens[i+1][0]+" is unknown")
            input.fill_(good_word.item())
            output, hidden = model(input, hidden)
            for j in range(1, len(good_tokens[i+1])): 
                next_token=dictionary_corpus.tokenize_str(dictionary,good_tokens[i+1][j])[0]
                if good_tokens[i+1][j] not in dictionary.word2idx:
                    print("Good word "+good_tokens[i+1][j]+" is unknown")
                input.fill_(next_token.item())
                output, hidden = model(input, hidden)
            results_list.append(results)
        result.append((sentence, results_list))
    return(result)
