#!/usr/bin/env python3

import argparse
import pip
import os
import wget
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser(description='Download and set-up files needed for Maze Automation. Specify which models to set-up')

parser.add_argument('--gulordava', help="For gulordava model", action="store_true")
parser.add_argument('--french', help="for French model", action="store_true")

args = parser.parse_args()
# need to check that all needed modules are installed
# download and place files

def download_gulordava():
    check=check_pkgs(['torch'])
    if check:
        make_dirs(['gulordava_code', 'gulordava_data'])
        if not os.path.exists('gulordava_code/utils.py'):
            wget.download('https://raw.githubusercontent.com/facebookresearch/colorlessgreenRNNs/master/src/language_models/utils.py', 'gulordava_code/utils.py')
        if not os.path.exists('gulordava_code/model.py'):
            wget.download('https://raw.githubusercontent.com/facebookresearch/colorlessgreenRNNs/master/src/language_models/model.py', 'model.py')
        if not os.path.exists('gulordava_data/hidden650_batch128_dropout0.2_lr20.0.pt'):
            wget.download('https://dl.fbaipublicfiles.com/colorless-green-rnns/best-models/English/hidden650_batch128_dropout0.2_lr20.0.pt', 'gulordava_data/hidden650_batch128_dropout0.2_lr20.0.pt')
        if not os.path.exists('gulordava_data/vocab.txt'):
            wget.download('https://dl.fbaipublicfiles.com/colorless-green-rnns/training-data/English/vocab.txt', 'gulordava_data/vocab.txt')
        print("Gulordava model is ready!")
    else:
        print("Some required packages are missing. Please install packages and try again.")
    return

def download_french():
    check=check_pkgs(['torch'])
    if check:
        if not os.path.exists('french_data/frwac_dicts.json') and os.path.exists('french_data/model_frwac.pt'):
            print("The french model cannot be downloaded automatically at this time. You can get the files from https://drive.google.com/drive/folders/19xUZ83f9qcI1PVBdnEv-e6BscWXz_33F,",\
              "but may need to ask for access. Then put 'frwac_dict.json' and 'model_frwac.pt' in the french_data folder.")
        else:
            print("French model is ready!")
    else:
        print("Some required packages are missing. Please install packages and try again.")

def download_one_b():
    check=check_pkgs(['csv', 'argparse', 're', 'sys', 'tensorflow', 'numpy'])
    if check:
        make_dirs(['one_b_code','one_b_data'])
        if not os.path.exists('one_b_code/data_utils.py'):
            wget.download('https://raw.githubusercontent.com/tensorflow/models/master/research/lm_1b/data_utils.py', 'one_b_code/data_utils.py')
        if not os.path.exists('one_b_data/ckpt-base'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-base', 'one_b_data/ckpt-base')
        if not os.path.exists('one_b_data/ckpt-char-embedding'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-char-embedding', 'one_b_data/ckpt-char-embedding')
        if not os.path.exists('one_b_data/ckpt-lstm'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-lstm', 'one_b_data/ckpt-lstm')
        if not os.path.exists('one_b_data/ckpt-softmax0'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax0', 'one_b_data/ckpt-softmax0')
        if not os.path.exists('one_b_data/ckpt-softmax1'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax1', 'one_b_data/ckpt-softmax1')
        if not os.path.exists('one_b_data/ckpt-softmax2'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax2', 'one_b_data/ckpt-softmax2')
        if not os.path.exists('one_b_data/ckpt-softmax3'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax3', 'one_b_data/ckpt-softmax3')
        if not os.path.exists('one_b_data/ckpt-softmax4'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax4', 'one_b_data/ckpt-softmax4')
        if not os.path.exists('one_b_data/ckpt-softmax5'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax5', 'one_b_data/ckpt-softmax5')
        if not os.path.exists('one_b_data/ckpt-softmax6'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax6', 'one_b_data/ckpt-softmax6')
        if not os.path.exists('one_b_data/ckpt-softmax7'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax7', 'one_b_data/ckpt-softmax7')
        if not os.path.exists('one_b_data/ckpt-softmax8'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/all_shards-2016-09-10/ckpt-softmax8', 'one_b_data/ckpt-softmax8')
        if not os.path.exists('one_b_data/graph-2016-09-10.pbtxt'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/graph-2016-09-10.pbtxt', 'one_b_data/graph-2016-09-10.pbtxt')
        if not os.path.exists('one_b_data/vocab-2016-09-10.txt'):
            wget.download('http://download.tensorflow.org/models/LM_LSTM_CNN/vocab-2016-09-10.txt', 'one_b_data/vocab-2016-09-10.txt')  
    else:
        print("Some required packages are missing. Please install packages and try again.")


def check_pkgs(packages):
    '''Given a list of packages, checks if they are installed
    If one is not installed, displays an error
    If any not installed, returns -1, else returns 1'''
    value=True
    for p in packages:
        try:
            __import__(p)
        except:
            print ("Needed package "+p+" is not installed.")
            value=False
    return value

def make_dirs(paths):
    '''Checks if paths exist, and if not creates them
    No return'''
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
    return
        
            
if args.gulordava:
    download_gulordava()
elif args.french:
    download_french()
check_pkgs(['wordfreq','nltk'])
