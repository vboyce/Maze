import torch
from nltk.tokenize import word_tokenize
from gulordava_code import dictionary_corpus
from helper import get_alt_nums, get_alts, strip_end_punct #combining helper helper_wf
#### gulordava specific ####
def load_model(freq):
    '''sets up a model for gulordava
    Arguments: none
    Returns the model and device'''
    with open("gulordava_data/hidden650_batch128_dropout0.2_lr20.0.pt", 'rb') as f:
        print("Loading the model")
        # to convert model trained on cuda to cpu model
        model = torch.load(f, map_location=lambda storage, loc: storage)
    model.eval() #put model in eval mode
    model.cpu() # put it on cpu
    device = torch.device("cpu") #what sort of data model is stored on
    return (model, device)

def load_dict():
    '''loads the dictionary
    Arguments: none
    Returns dictionary and length of dictionary'''
    dictionary = dictionary_corpus.Dictionary("gulordava_data") #load a dictionary
    ntokens = dictionary.__len__() #length of dictionary
    return(dictionary, ntokens)

def new_sentence(model, device, ntokens):
    '''sets up a new sentence for gulordava model
    Arguments: model, device as from load_model, ntokens = length of dictionary
    returns a word placeholder and an initialized hidden layer'''
    hidden = model.init_hidden(1) #sets initial values on hidden layer
    input_word = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device) #make a word placeholder
    return (input_word, hidden)

def update_sentence(word, input_word, model, hidden, dictionary):
    '''takes in a sentence so far adds the next word and returns the new list of surprisals
    Arguments:
    word = next word in sentence
    input_word = placeholder for wordid
    model = model from load_model
    hidden = hidden layer representation of sentence so far
    dictionary = dictionary from load_dict
    Returns: output = (probably not needed??)
    hidden = new hidden layer
    word_surprisals = distribution of surprisals for all words'''
    parts = word_tokenize(word) #get list of tokens
    for part in parts:
        token = dictionary_corpus.tokenize_str(dictionary, part)[0] #get id of token
        if part not in dictionary.word2idx:
            print("Good word "+part+" is unknown") #error message
        input_word.fill_(token.item()) #fill with value of token
        output, hidden = model(input_word, hidden) #do the model thing
        word_weights = output.squeeze().div(1.0).exp().cpu() #process output into weights
        word_surprisals = -1*torch.log2(word_weights/sum(word_weights))# turn into surprisals
    return (hidden, word_surprisals)

def get_surprisal(surprisals, dictionary, word):
    '''Find the surprisal for a word given a context
    Arguments:
    surprisals - surprisal distribution
    dictionary - word to word id dictionary
    word - word we want surprisal for 
    Returns the numeric surprisal value of the word, if word is unknown returns -1
    We don't trust surprisal values for UNK words'''
    token = dictionary_corpus.tokenize_str(dictionary, word)[0] #take first token of word
    if word not in dictionary.word2idx:
        print(word+" is unknown")
        return -1 #use -1 as an error code
    return surprisals[token].item() #numeric value of word's surprisal

