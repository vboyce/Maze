import os
import sys

import numpy as np
from six.moves import xrange
import tensorflow as tf
from nltk.tokenize import word_tokenize
from google.protobuf import text_format
from one_b_code import data_utils

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


def Surprisal(sentence_input):
    '''returns the surprisal of the last word given prior words as context'''
    vocab=data_utils.CharsVocabulary("one_b_data/vocab-2016-09-10.txt", MAX_WORD_LEN)
    targets = np.zeros([BATCH_SIZE, NUM_TIMESTEPS], np.int32)
    weights = np.ones([BATCH_SIZE, NUM_TIMESTEPS], np.float32)

    # Load the model with the given pbtxt file and the checkpoint files
    sess, t = _LoadModel("one_b_data/graph-2016-09-10.pbtxt", "one_b_data/ckpt-*")

    result = []
    
    for j in range(len(sentence_input)):
        print("One_b "+str(j))
        good_sentence,alts=sentence_input[j]

        inputs = np.zeros([BATCH_SIZE, NUM_TIMESTEPS], np.int32)
        char_ids_inputs = np.zeros( [BATCH_SIZE, NUM_TIMESTEPS, vocab.max_word_length], np.int32)
        
        good_words=good_sentence.split()
        good_tokens=[word_tokenize(x) for x in good_words]
        #sent = [vocab.word_to_id(w) for w in good_sentence.split()]
        #sent_char_ids = [vocab.word_to_char_ids(w) for w in good_sentence.split()]

        #samples = sent[:]
        #char_ids_samples = sent_char_ids[:]
        firstword=vocab.word_to_id(good_tokens[0][0])
        firstword_char=vocab.word_to_char_ids(good_tokens[0][0])
        if firstword==vocab.unk:
            print("Good word "+good_tokens[0][0]+" is unknown")
        inputs[0, 0] = firstword
        char_ids_inputs[0, 0, :] = firstword_char
        total_surprisal = 0

        for j in range(1, len(good_tokens[0])): 
            softmax = sess.run(t['softmax_out'],
                                     feed_dict={t['char_inputs_in']: char_ids_inputs,
                                                t['inputs_in']: inputs,
                                                t['targets_in']: targets,
                                                t['target_weights_in']: weights})
            next_token=vocab.word_to_id(good_tokens[0][j])
            if next_token==vocab.unk:
                print("good word "+good_tokens[0][j]+" is unknown")
            next_token_chars=vocab.word_to_char_ids(good_tokens[0][j])
            word_surprisal=-1 * np.log2(softmax[0][next_token])
            total_surprisal+=word_surprisal
            inputs[0,0]=next_token
            char_ids_inputs[0,0,:]=next_token_chars


        results_list=[]
        good_results=[]
        suggest_list=[]
        for i in range(len(alts)):
            results={}
            softmax = sess.run(t['softmax_out'],
                                     feed_dict={t['char_inputs_in']: char_ids_inputs,
                                                t['inputs_in']: inputs,
                                                t['targets_in']: targets,
                                                t['target_weights_in']: weights})
            for k in range(len(alts[i])):
                test_word=alts[i][k]
                test_token=vocab.word_to_id(test_word)
                if test_token==vocab.unk:
                    print(test_word+" is unknown")
                    results[test_word]=-1
                else:
                    results[test_word]=-1 * np.log2(softmax[0][test_token])
            results_list.append(results)
            suggest=[]
            for l in range(5):
                sample = _SampleSoftmax(softmax[0])
                suggest.append(vocab.id_to_word(sample))
            suggest_list.append(suggest)
            good_word_token=vocab.word_to_id(good_tokens[i+1][0])
            if good_word_token==vocab.unk:
                print("Good word "+good_tokens[i+1][0]+" is unknown")
            good_word_chars=vocab.word_to_char_ids(good_tokens[i+1][0])
            word_surprisal=-1 * np.log2(softmax[0][good_word_token])
            total_surprisal+=word_surprisal
            good_results.append(word_surprisal)
            inputs[0, 0] = good_word_token
            char_ids_inputs[0, 0, :] = good_word_chars
            for j in range(1, len(good_tokens[i+1])): 
                softmax = sess.run(t['softmax_out'],
                                         feed_dict={t['char_inputs_in']: char_ids_inputs,
                                                    t['inputs_in']: inputs,
                                                    t['targets_in']: targets,
                                                    t['target_weights_in']: weights})                
                next_token=vocab.word_to_id(good_tokens[i+1][j])
                if next_token==vocab.unk:
                    print("Good word "+good_tokens[i+1][j]+" is unknown")
                next_token_chars=vocab.word_to_char_ids(good_tokens[i+1][j])
                word_surprisal = -1 * np.log2(softmax[0][next_token])
                total_surprisal+=word_surprisal
                inputs[0,0]=next_token
                char_ids_inputs[0,0,:]=next_token_chars

        result.append((good_sentence,good_results, results_list,suggest_list))
    return(result)

