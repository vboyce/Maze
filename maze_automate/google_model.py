
import re
import sys
import logging
import tensorflow as tf
import numpy as np
from google.protobuf import text_format
from lang_model import lang_model
from one_b_code import data_utils

class google_model(lang_model):
    """Wrapping class for google model"""

    def __init__(self):
        """Do whatever set-up it takes"""
        with tf.Graph().as_default():
            with tf.gfile.FastGFile("one_b_data/graph-2016-09-10.pbtxt", 'r') as f:
                s = f.read()
                gd = tf.GraphDef()
                text_format.Merge(s, gd)
            tf.logging.info('Recovering Graph %s', "one_b_data/graph-2016-09-10.pbtxt")
            self.t = {}
            [self.t['states_init'], self.t['lstm/lstm_0/control_dependency'],
             self.t['lstm/lstm_1/control_dependency'], self.t['softmax_out'], self.t['class_ids_out'],
             self.t['class_weights_out'], self.t['log_perplexity_out'], self.t['inputs_in'],
             self.t['targets_in'], self.t['target_weights_in'], self.t['char_inputs_in'],
             self.t['all_embs'], self.t['softmax_weights'], self.t['global_step']
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
            self.sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
            self.sess.run('save/restore_all', {'save/Const:0': "one_b_data/ckpt-*"})
            self.sess.run(self.t['states_init'])
            self.dictionary = data_utils.CharsVocabulary("one_b_data/vocab-2016-09-10.txt", 50)

    def tokenize(self, word):
        """ returns a list of tokens according to the models desired tokenization scheme"""
        new_string = re.sub("([.,?!])", r" \1 ", word)  # split some punctuation as their own words
        newer_string = re.sub("'", " '", new_string)  # split words before apostrophes
        tokens = newer_string.split()
        return tokens

    def empty_sentence(self):
        """Initialize a new sentence -- starter hidden state etc"""
        targets = np.zeros([1, 1], np.int32)
        weights = np.ones([1, 1], np.float32)
        hidden = {"targets":targets, "weights":weights}
        return hidden

    def update(self, hidden, word):
        """Given the model representation (=hidden state) and the next word (not tokenized)
        returns new hidden state (at end of adding word)
        and probability distribution of next words at end of addition"""
        parts = self.tokenize(word)  # get list of tokens
        inputs = np.zeros([1, 1], np.int32)
        char_ids_inputs = np.zeros([1, 1, self.dictionary.max_word_length], np.int32)
        targets=hidden["targets"]
        weights=hidden["weights"]
        for part in parts:
            token = self.dictionary.word_to_id(part)  # get id of token
            char_tokens = self.dictionary.word_to_char_ids(part)  # get char ids
            if token == self.dictionary.unk:
                logging.warning('%s is not in the Jozefowicz model vocabulary.', part)
            inputs[0, 0] = token
            char_ids_inputs[0, 0, :] = char_tokens
            softmax = self.sess.run(self.t['softmax_out'],  # run the model
                               feed_dict={self.t['char_inputs_in']: char_ids_inputs,
                                          self.t['inputs_in']: inputs,
                                          self.t['targets_in']: targets,
                                          self.t['target_weights_in']: weights})
        #surprisal = tf.math.log(softmax)*np.log2(np.e)
        surprisal=[]
        hidden={"targets":targets, "weights":weights}
        return hidden,surprisal,softmax  # not sure we need to return targets

    def get_surprisal(self, surprisals,softmax, word):
        """Given a probability distribution, and a word
        Return its surprisal (bits), or use something as unknown code"""
        token = self.dictionary.word_to_id(word)  # take first token of word
        if token == self.dictionary.unk:
            print(word + " is unknown")
            return -1  # use -1 as an error code
        return -1 * np.log2(softmax[0][token])  # numeric value of word's surprisal
