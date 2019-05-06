''' one_b model specific modules'''

import re
import sys
import tensorflow as tf
import numpy as np
from google.protobuf import text_format
from one_b_code import data_utils


from helper import get_alt_nums, get_alts, strip_end_punct
#### One b specific ####
def load_model():
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

def load_dict():
    '''get the dictionary used by one_b'''
    dictionary = data_utils.CharsVocabulary("one_b_data/vocab-2016-09-10.txt", 50)
    return dictionary

def new_sentence(dictionary):
    '''initializes a new blank sentence'''
    targets = np.zeros([1, 1], np.int32)
    weights = np.ones([1, 1], np.float32)
    inputs = np.zeros([1, 1], np.int32)
    char_ids_inputs = np.zeros([1, 1, dictionary.max_word_length], np.int32)
    return (targets, weights, inputs, char_ids_inputs)

def tokenize(word):
    '''takes a word, returns it split into tokens to match tokenization that one_b model expects'''
    new_string = re.sub("([.,?!])", r" \1 ", word) # split some punctuation as their own words
    newer_string = re.sub("'", " '", new_string) # split words before apostrophes
    tokens = newer_string.split()
    return tokens

def update_sentence(word, inputs, char_ids_inputs, sess, t, targets, weights, dictionary):
    '''takes in a sentence, adds the next word and returns the new list of surprisals
    Arguments:
    word = next word in sentence,
    inputs = placeholder for word,
    char_ids_inputs = placeholder for word's characters,
    sess, t from load_model,
    targets, weights are describing the sentence so far,
    dictionary is word to id lookup
    Returns:
    targets, weights = representation of new sentence,
    softmax = distribution over next word surprisals'''
    parts = tokenize(word) #get list of tokens
    for part in parts:
        token = dictionary.word_to_id(part)#get id of token
        char_tokens = dictionary.word_to_char_ids(part) #get char ids
        if token == dictionary.unk:
            print("Good word "+part+" is unknown") #error message
        inputs[0, 0] = token
        char_ids_inputs[0, 0, :] = char_tokens
        softmax = sess.run(t['softmax_out'], # run the model
                           feed_dict={t['char_inputs_in']: char_ids_inputs,
                                      t['inputs_in']: inputs,
                                      t['targets_in']: targets,
                                      t['target_weights_in']: weights})
    return (targets, weights, softmax) # not sure we need to return targets

def get_surprisal(softmax, dictionary, word):
    '''given the surprisal distribution, a dictionary (word to word ids), and a word
    returns the numeric surprisal value of the word, if word is unknown returns -1
    We don't trust surprisal values for UNK words'''
    token = dictionary.word_to_id(word) #take first token of word
    if token == dictionary.unk:
        print(word+" is unknown")
        return -1 #use -1 as an error code
    return -1 * np.log2(softmax[0][token]) #numeric value of word's surprisal

def find_bad_enough(num_to_test, minimum, word_list, surprisals_list, dictionary):
    '''will return the word that is at least minimum surprisal for all sentences. if goes through num_to_test words
    without finding a bad enough, returns the worst it's seen (worst = highest min)
    inputs: num_to_test - an integer for how many candidate words to try,
    minimum = minimum suprisal to look for (will return first word with at least this surprisal for all sentences)
    word_list = the good words that occur in this position
    surprisals_list = distribution of probabilities (from update_sentence)
    dictionary = word to word id lookup
    returns: a word that meets the surprisal target or the best option if num_to_test have been tested and none have met minimum'''
    best_word = ""
    best_surprisal = 0
    length, freq = get_alt_nums(word_list) # find what length and frequency is average for good words
    options_list = None
    i = 0
    k = 0
    while options_list is None:
        options_list = get_alts(length, freq+i) # find words with that length and frequency
        i += 1 #if there weren't any, try a slightly higher frequency
    while best_surprisal == 0 or k < num_to_test: #no word has a real surprisal value or we haven't tested enough
        min_surprisal = 100 #dummy value higher than we expect any surprisal to actually be
        if k == len(options_list): # if we run out of options
            new_options = None
            while new_options is None:
                new_options = get_alts(length, freq+i) #keep trying to find higher frequency words
                i += 1
            options_list.extend(new_options) #add to the options list
        word = options_list[k] #try the kth option
        k += 1
        for j, _ in enumerate(surprisals_list): # for each sentence this word needs to fit
            surprisal = get_surprisal(surprisals_list[j], dictionary, word) #find that word on the list
            min_surprisal = min(min_surprisal, surprisal) #lowest surprisal we've seen so far in this sentence list
        if min_surprisal >= minimum: #if surprisal in each condition is greater than required
            return word # we found a word to use and are done here
        if min_surprisal > best_surprisal: #if it's the best option so far, record that
            best_word = word
            best_surprisal = min_surprisal
    print("Couldn't meet surprisal target, returning with surprisal of "+str(best_surprisal)) # if we've run through our list, return the best we have, but warn about it
    return best_word

def do_sentence_set(sentence_set, sess, t, dictionary):
    '''Gets distractors for a set of sentences that all get the same distractors
    arguments: sentence_set = a list of sentences (all equal length)
    sess, t = from load_model
    dictionary = from load_dictionary
    returns a sentence format string of the distractors'''
    bad_words = []
    words = []
    sentence_length = len(sentence_set[0].split()) # length of each sentence
    for i, _ in enumerate(sentence_set):
        bad_words.append(["x-x-x"])
        sentence = sentence_set[i]
        sent_words = sentence.split() # turn sentence into words
        if len(sent_words) != sentence_length: # complain if there are inconsistent lengths
            print("inconsistent lengths!!")
        words.append(sent_words) # make a list of list of words
    inputs = [None]*len(sentence_set) # initialize a bunch of things
    char_ids_inputs = [None]*len(sentence_set)
    weights = [None]*len(sentence_set)
    targets = [None]*len(sentence_set)
    softmaxes = [None]*len(sentence_set)
    for i in range(len(sentence_set)):
        targets[i], weights[i], inputs[i], char_ids_inputs[i] = new_sentence(dictionary)
    for j in range(sentence_length-1): # for each word position
        word_list = []
        for i in range(len(sentence_set)): # for each sentence
            targets[i], weights[i], softmaxes[i] = update_sentence(words[i][j], inputs[i], char_ids_inputs[i], sess, t, targets[i], weights[i], dictionary) # add a word to the sentence
            word_list.append(words[i][j+1]) # make a list of the 'good' next words
        bad_word = find_bad_enough(100, 21, word_list, softmaxes, dictionary) # for a distractor word for that position, using the probability distributions and the good words. Try 100 options, aim for surprisal of at least 21
        for l, _ in enumerate(sentence_set):
                cap=word_list[l][0].isupper() # what is capitization of good word in ith sentence
                if cap: #capitalize it
                    mod_bad_word=bad_word[0].upper()+bad_word[1:]
                else: #keep lower case
                    mod_bad_word=bad_word
                mod_bad_word = mod_bad_word+strip_end_punct(word_list[l])[1] #match end punctuation
                bad_words[l].append(mod_bad_word) # add the fixed bad word to a running list for that sentence
    bad_sentences=[]
    for i, _ in enumerate(bad_words):
        bad_sentences.append(" ".join(bad_words[i]))
    return bad_sentences # and return
