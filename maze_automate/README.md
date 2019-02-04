# Autogenerating Maze materials

## Set up
Depending on which model you plan on running, you will need different things installed. 

### Gulordava model
You will need to install some packages. For the Gulordava model, you will need pytorch (pytorch.org) and NLTK (https://www.nltk.org/install.html, use pip3 and not pip). In a python shell, run import ntlk and then nltk.download('punkt')

In maze_automate create a folder called gulordava_code. From https://github.com/facebookresearch/colorlessgreenRNNs copy src/language_models/utils.py 

In maze_automate also create a folder called gulordava_data. From https://github.com/facebookresearch/colorlessgreenRNNs/tree/master/data download the pre-trained english model. Put hidden650_batch128_dropout0.2_lr20.0.pt in this folder. Also download and add the English vocabulary data (vocab.txt)

In maze_automate add the file /src/language_models/model.py . 

### One_b model
Install tensorflow (pip3 install tensorflow)

Create a folder one_b_code and download https://github.com/tensorflow/models/blob/master/research/lm_1b/data_utils.py into there. 

Create a folder one_b_data and download the sharded checkpoints, the model graphdef file, the vocab file,  from https://github.com/tensorflow/models/blob/master/research/lm_1b/README.md

### Rebuilding lexicon

For a first run, you shouldn't need to do anything. However, code and files are included to rebuild the word to frequency look-ups and reverse. If you want to use another source for frequency data, use different cut-offs, change which words can be used for distractors, or if you find words that need their frequencies fixed, you can. 

All of this is taken care of in lexicon_generator.py. To avoid repeating long processes, many of the outputs are saved as json serialized objects (.json files). 

To redo everything from scratch:
1) build a list of distractor-okay words with make_word_list . If words you don't think are wordlike enough are showing up as distractors, edit exclude.txt (add the words you don't want included), and rerun make_word_list.
2) read frequency information from google ngrams (this takes a while). Unless you are completely changing what source is used or changing what criteria are used to define word (for recognizing in materials), you shouldn't need to do this. If you do, download all the alpha-character unigram files from http://storage.googleapis.com/books/ngrams/books/datasetsv2.html and save them in Maze/unigram/ . Run parse_files which will save everything to unigram_raw.json.
3) overriding the frequency of some words (contractions). The google ngrams corpus is generally reasonable about word frequencies, however when it parses things differently from how people do, there can be problems. In particular, it usually parses contractions as multiple words, so assigns unrealistically low frequencies to contractions. To fix this, we manually override contraction frequencies with the "contractions.csv" file. If you need to fix frequencies with other words, edit contractions.csv to add new words and floor log base 2 estimates of their occurance. (Look up frequencies of words in the dictionary and their frequencies in your source and do some math.) Contraction frequencies were generated using the google ngrams viewer. No need to re_run anything additional. 
4) Changing length or frequency cut offs. Edit the code in make_lexicon. 

After doing any of these, you will need to run save_things. 
