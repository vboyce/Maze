import torch
import logging
import re
from lang_model import lang_model
from french_code import dict_utils
import utils
import sys  # because pickle is dumb and can't deal with things in other locations

sys.path.insert(0, './french_code')


class french_model(lang_model):
    """Wrapping class for gulordava model"""

    def __init__(self):
        """Do whatever set-up it takes"""
        with open("french_data/model_frwac.pt", 'rb') as f:
            print("Loading the model")
            # to convert model trained on cuda to cpu model
            self.model = torch.load(f, map_location=lambda storage, loc: storage)
        self.model.eval()  # put model in eval mode
        self.model.cpu()  # put it on cpu
        self.device = torch.device("cpu")  # what sort of data model is stored on
        self.dictionary = dict_utils.Dictionary()
        self.dictionary.load("french_data/frwac_dicts.json")# load a dictionary
        self.ntokens = len(self.dictionary)  # length of dictionary

    def tokenize(self, word):
        """ returns a list of tokens according to the models desired tokenization scheme"""
        new_string = re.sub("([.,?!])", r" \1 ", word)  # split some punctuation as their own words
        newer_string = re.sub("'", "' ", new_string)  # split words after apostrophes
        tokens = newer_string.split()
        return tokens

    def empty_sentence(self):
        """Initialize a new sentence -- starter hidden state etc"""
        hidden = self.model.init_hidden(1)  # sets initial values on hidden layer
        return hidden

    def update(self, hidden, word):
        """Given the model representation (=hidden state) and the next word (not tokenized)
        returns new hidden state (at end of adding word)
        and probability distribution of next words at end of addition"""
        input_word = torch.randint(self.ntokens, (1, 1), dtype=torch.long).to(self.device)  # make a word placeholder
        parts = self.tokenize(word)  # get list of tokens
        for part in parts:
            if part not in self.dictionary.word2idx:
                logging.warning('%s is not in the French model vocabulary.', part)
                token=self.dictionary.word2idx["UNK"]
            else:
                token = self.dictionary.word2idx[part]
            input_word.fill_(token)  # fill with value of token
            output, hidden = self.model(input_word, hidden)  # do the model thing
            word_weights = output.squeeze().div(1.0).exp().cpu()  # process output into weights
            word_surprisals = -1 * torch.log2(word_weights / sum(word_weights))  # turn into surprisals
        return hidden, word_surprisals

    def get_surprisal(self, surprisals, word):
        """Given a probability distribution, and a word
        Return its surprisal (bits), or use something as unknown code"""
        word_tokens = self.tokenize(word)
        if len(word_tokens) > 1:
            logging.warning('Word %s is multi-token.', word)
        if word_tokens[0] not in self.dictionary.word2idx:
            logging.info('Word %s has unknown first token %s.', word, word_tokens[0])
            return 0  # use 0 as an error code
        token=self.dictionary.word2idx[word_tokens[0]]
        return surprisals[token].item()  # numeric value of word's surprisal
