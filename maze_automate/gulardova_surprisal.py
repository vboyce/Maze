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


def Surprisal(sentence_input):
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
        sentence, alts=sentence_input[j]
        
        torch.manual_seed(1111)
        hidden = model.init_hidden(1)
        input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device)
        
        good_words=sentence.split()
        good_tokens=[word_tokenize(x) for x in good_words]
        print(good_tokens)
        totalsurprisal = 0
        firstword = dictionary_corpus.tokenize_str(dictionary,good_tokens[0][0])[0]
        if good_tokens[0][0] not in dictionary.word2idx:
            print("Good word "+good_tokens[0][0]+" in unknown")
        input.fill_(firstword.item())
        output, hidden = model(input,hidden)        
        word_weights = output.squeeze().div(1.0).exp().cpu()
        word_surprisals = -1*torch.log2(word_weights/sum(word_weights))
        
        for j in range(1, len(good_tokens[0])): 
            next_token=dictionary_corpus.tokenize_str(dictionary,good_tokens[0][j])[0]
            if good_tokens[0][j] not in dictionary.word2idx:
                print("Good word "+good_tokens[0][j]+" is unknown")
            word_surprisal = word_surprisals[next_token].item()  
            totalsurprisal = word_surprisal + totalsurprisal
            input.fill_(next_token.item())
            output, hidden = model(input, hidden)
            word_weights = output.squeeze().div(1.0).exp().cpu()
            word_surprisals = -1*torch.log2(word_weights/sum(word_weights))
            
        results_list=[]
        good_results=[]
        suggest_list=[]
        for i in range(len(alts)):
            results={}
            for k in range(len(alts[i])):
                test_word=alts[i][k] #word being tested
                test_token=dictionary_corpus.tokenize_str(dictionary, test_word)[0]
                if test_word not in dictionary.word2idx:
                    print(test_word+" is unknown")
                    results[test_word]=-1
                else:
                    results[test_word]=word_surprisals[test_token].item()
            results_list.append(results)
            suggest=[]
            for l in range(5):
                sample = torch.multinomial(word_weights, 1)[0]
                suggest.append((dictionary.idx2word[sample]))
            suggest_list.append(suggest)
            good_word=dictionary_corpus.tokenize_str(dictionary,good_tokens[i+1][0])[0]
            if good_tokens[i+1][0] not in dictionary.word2idx:
                print("Good word "+good_tokens[i+1][0]+" is unknown")
            word_surprisal = word_surprisals[good_word].item()  
            totalsurprisal = word_surprisal + totalsurprisal
            input.fill_(good_word.item())
            output, hidden = model(input, hidden)
            word_weights = output.squeeze().div(1.0).exp().cpu()
            word_surprisals = -1*torch.log2(word_weights/sum(word_weights))
            good_results.append(word_surprisal)
            for j in range(1, len(good_tokens[i+1])): 
                next_token=dictionary_corpus.tokenize_str(dictionary,good_tokens[i+1][j])[0]
                if good_tokens[i+1][j] not in dictionary.word2idx:
                    print("Good word "+good_tokens[i+1][j]+" is unknown")
                word_surprisal = word_surprisals[next_token].item()  
                totalsurprisal = word_surprisal + totalsurprisal
                input.fill_(next_token.item())
                output, hidden = model(input, hidden)
                word_weights = output.squeeze().div(1.0).exp().cpu()
                word_surprisals = -1*torch.log2(word_weights/sum(word_weights))
        result.append((sentence, good_results, results_list, suggest_list))
    return(result)
