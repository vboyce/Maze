# Copyright (c) 2018-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#


import torch
import torch.nn as nn
import torch.nn.functional as F

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
    for j in range(len(sentence_list)):
        print("Gulardova "+str(j))
        sentence, alts=sentence_list[j]
        
        torch.manual_seed(1111)
        hidden = model.init_hidden(1)
        input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device)

        good_sentence = dictionary_corpus.tokenize_str(dictionary,sentence)
        totalsurprisal = 0
        firstword = good_sentence[0]

        input.fill_(firstword.item())
        output, hidden = model(input,hidden)        
        word_weights = output.squeeze().div(1.0).exp().cpu()
        word_surprisals = -1*torch.log2(word_weights/sum(word_weights))

        results_list=[]
        good_results=[]
        for i in range(len(alts)):
            results={}
            for k in range(len(alts[i]):
                test_word=alts[i][k] #word being tested
                results[test_word]=word_surprisals[word].item()
            results_list.append(results)
            good_word=good_sentence[i+1]
            word_surprisal = word_surprisals[word].item()  
            totalsurprisal = word_surprisal + totalsurprisal
            input.fill_(word.item())
            output, hidden = model(input, hidden)
            word_weights = output.squeeze().div(1.0).exp().cpu()
            word_surprisals = -1*torch.log2(word_weights/sum(word_weights))
            good_results.append(word_surprisal)
        result.append((good_sentence, good_results, results_list))
    return(result)
