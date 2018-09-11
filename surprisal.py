import os
import sys

import numpy as np
from six.moves import xrange
import tensorflow as tf

from google.protobuf import text_format
import data_utils

# For saving demo resources, use batch size 1 and step 1.
BATCH_SIZE = 1
NUM_TIMESTEPS = 1
MAX_WORD_LEN = 50


def _LoadModel(gd_file, ckpt_file):
  """Load the model from GraphDef and Checkpoint.

  Args:
    gd_file: GraphDef proto text file.
    ckpt_file: TensorFlow Checkpoint file.

  Returns:
    TensorFlow session and tensors dict.
  """
  with tf.Graph().as_default():
    sys.stderr.write('Recovering graph.\n')
    with tf.gfile.FastGFile(gd_file, 'r') as f:
      s = f.read()
      gd = tf.GraphDef()
      text_format.Merge(s, gd)

    tf.logging.info('Recovering Graph %s', gd_file)
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

    sys.stderr.write('Recovering checkpoint %s\n' % ckpt_file)
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    sess.run('save/restore_all', {'save/Const:0': ckpt_file})
    sess.run(t['states_init'])

  return sess, t


def Context_Surprisal(sentence):
    '''returns the surprisal of the last word given prior words as context'''
    vocab=data_utils.CharsVocabulary("../data/vocab-2016-09-10.txt", MAX_WORD_LEN)
    targets = np.zeros([BATCH_SIZE, NUM_TIMESTEPS], np.int32)
    weights = np.ones([BATCH_SIZE, NUM_TIMESTEPS], np.float32)

    # Load the model with the given pbtxt file and the checkpoint files
    sess, t = _LoadModel("../data/graph-2016-09-10.pbtxt", "../data/ckpt-*")

    result = []
    inputs = np.zeros([BATCH_SIZE, NUM_TIMESTEPS], np.int32)
    char_ids_inputs = np.zeros( [BATCH_SIZE, NUM_TIMESTEPS, vocab.max_word_length], np.int32)
    
    sent = [vocab.word_to_id(w) for w in sentence.split()]
    sent_char_ids = [vocab.word_to_char_ids(w) for w in sentence.split()]

    samples = sent[:]
    char_ids_samples = sent_char_ids[:]

    total_surprisal = 0

    for n in range(len(sentence.split(" "))-1):
            inputs[0, 0] = samples[0]
            char_ids_inputs[0, 0, :] = char_ids_samples[0]
            samples = samples[1:]
            char_ids_samples = char_ids_samples[1:]
            softmax = sess.run(t['softmax_out'],
                                 feed_dict={t['char_inputs_in']: char_ids_inputs,
                                            t['inputs_in']: inputs,
                                            t['targets_in']: targets,
                                            t['target_weights_in']: weights})

            surprisal = -1 * np.log2(softmax[0][sent[n+1]])
            total_surprisal += surprisal
    return(surprisal)
