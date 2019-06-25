# Autogenerating Maze materials

Code provided here takes experimental materials (such as used for SPR) and generates distractor words for each position of each sentence. Minimal pair sentences (i.e. same sentence in two or more different conditions) can be set to recieve the same distractors in each word psotion if they are the same length, by giving them the same item number. (This is currently the only way of automatically matching distractors between sentences; more complicated things may be implementated at a later date.)

Distractor words are selected to be roughly length and frequency matched with the good word in the sentence (or if matching multiple, the average for the good words), but have high surprisal in the context or contexts, as determined by the model. They are not necessarily ungrammatical (but often are). 

Distractors will have end punctuation and capitalization that matches their good word. (In the rare case of minimal pair sentences that in part differ in punctuation and capitalization, distractors will match indiviual words, and thus differ across sentences, but only in punctuation and capitalization.)

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

## Frequency data sources

There are two options for where to get word frequency information (used for matching distractors to real words) from. Either the 'original' sum up counts from the google ngrams unigrams list method, or a new option that just uses wordfreq (https://pypi.org/project/wordfreq/).

### Ngrams options
Downsides:
 - contraction frequencies were read off of google ngrams viewer and entered manually
 - overestimates the frequency of old words ('thy' etc.) and therefore will choose these as frequent distractors
 - Can't handle OOV items at all (All words in your materials need to be in the overall dictionary (built from google ngrams). If they are not, you should consider fixing them (for compound words, try without hyphens).)
 
Upside:
 - Forthcoming paper used this method, so it's been tested and works
 
### Wordfreq options
Downsides:
 - Need to install wordfreq (see https://pypi.org/project/wordfreq/ for instructions)
 - Corpus includes modern texts like Reddit, so it thinks expletives (and slang) are high frequency, and will choose them as frequent distractors (to keep words from showing up as distractors, add them to exclude_wf.txt, then from lexicon_generator_wf.py, uncomment and run the two lines at the bottom) (Alternatively, find a bowdlerized word list to use in place of words.txt)
 - Untested
 
Upsides:
 - Generation is quick, so it's easy to change bin sizes or add more words to the exclude list (if you change bin sizes, also change corresponding look-up calculations in helper_wf.py)
 - More representative distribution of words taken from more sources
 - Handles OOV words well (read https://pypi.org/project/wordfreq/ for how frequencies are extrapolated)

## Running
First, you need to make automate.py executable. In a terminal chmod +x automate.py.
Then can be run as ./automate.py . Note that, especially the one_b model, is computationally expensive to run, and you may want to use a computational cluster. Testing a couple sentences worth on a laptop will probably work okay. 

Arguments:
 - input (required) -- file with materials
 - output (required) -- file to write output to
 - model (default: gulordava) -- which model to use (either gulordava or one_b)
 - freq (default: ngrams) -- which source of frequency information to use either ngrams (counts processed out of google ngrams unigrams files) or wordfreq (uses python module wordfreq)
 - format (default: basic) -- which format to write results in; either basic for semicolon delimited (like the input file, but with an extra column for the distractors) or ibex (ready to copy into a .js ibex experiment file)

### Material format
See test_input.txt for a sample. Materials should be in semi-colon delimited format. 
 - Column 1: condition. This is not used at all for distractor generation, but is copied to output. For ibex format output, this is treated as the "condition"/group. Good to use to indicate practice/filler/which type of critical item.
 - Column 2: item number. Sentences with the same item number will recieve the same sequence of distractors (and need to be the same length). 
 - Column 3: The good sentence. 

### Output format
If you're running maze with ibex (using code provided in this repo), you will want to use maze output format. Then copy the results into the items list of the experiment file. A basic output format (like the input, but with an extra column for the distractors) is provided if the materials are being used on a different platform. 

## Making adjustments

### Problems with the lexicon
 The models will run reasonably even if their dictionaries (i.e, their training data) do not contain all the words; however when writing new materials, it might be worth sticking to their dictionaries.

You may need to rebuild the lexicons if:
 - words are showing up as distractors that you don't want/don't think are words
 - distractors seem to be the wrong frequency for good words (google ngrams may be giving an unreasonable frequency for the good word, especially if it could be parsed as multiple words)
 - you want to make other changes. 

All of this is handled in lexicon_generator.py. To avoid repeating long processes, many of the intermediate outputs are saved as json serialized objects (.json files), thus, if you are only changing what words are excluded from this distractor list, or what words have frequencies overriden, you won't need to regenerate everything. 

What lexicon_generator can do:
1) Build a list of acceptable distractor words (with make_word_list). If words you don't think are wordlike enough are showing up as distractors, edit exclude.txt (add the words you don't want included), and rerun make_word_list.
2) Read frequency information from google ngrams (this takes a while). Unless you are completely changing what source is used or changing what criteria are used to define word (for recognizing in materials), you shouldn't need to do this. If you do need to, download all the alpha-character unigram files from http://storage.googleapis.com/books/ngrams/books/datasetsv2.html and save them in Maze/unigram/ . Run parse_files which will regenerate unigram_raw.json.
3) Overriding the frequency of some words (contractions). The google ngrams corpus is generally reasonable about word frequencies, however when it parses things differently from how people do, there can be problems. In particular, it usually parses contractions as multiple words, so assigns unrealistically low frequencies to contractions. To fix this, we manually override contraction frequencies with the "contractions.csv" file. If you need to fix frequencies with other words, edit contractions.csv to add new words and floor log base 2 estimates of their occurance. Use get_freq to look up frequencies of some words for a baseline, and then compare their frequencies in another source to those of words you're fixing, and do some guessing or interpolation. Contraction frequencies come from google ngrams viewer. No need to rerun anything additional. 
4) Changing length or frequency cut offs. Edit the code in make_lexicon. No need to rerun anything additional.
After doing any of these, you will need to run save_things, to regenerate unigram.json and lexicon.json. 

### Changing thresholds
Distractor word selection for either model is set to try 100 words, and choose either the first word with surprisal of 21 or higher or none of the 100 words have surprisal of 21 or higher, the word with the highest. These values can be changed in the function  do_sentence_set of one_b.py or gulordava.py. 
