import os
from io import open
import torch
import json

class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)

    def load(self, path):
        assert os.path.exists(path)
        with open(path) as f:
            dicts = json.load(f)
        self.word2idx = dicts['word2idx']
        self.idx2word = dicts['idx2word']
