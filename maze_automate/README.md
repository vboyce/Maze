# Autogenerating Maze materials

(See Section 3 of [Maze Made Easy](https://psyarxiv.com/b7nqd/) for the motivation behind this approach, schematics of how it works, and some advice for its use.)

This code takes experimental materials (sets of sentences, such as for SPR) and generates distractors words for each position, returning A-maze materials. Distractor words are guaranteed to be (roughly) length- and frequency-matched to the target word(s); they are also guaranteed to be high surprisal under the language model. This will often mean they are ungrammatical or otherwise obvious mismatches to the context, but it's not guaranteed. 

## Set up
### Windows
1. Download the files by going to <https://github.com/vboyce/Maze>, clicking the green "Clone or Download" button, and selecting Download Zip. Once the zip file downloads, extract the maze_automate folder to the desired location. 
2. Install python3 and pip3 by going to https://www.python.org/downloads/windows/ and selecting under Stable Releases > (latest Python 3 version) > "Download Windows x86-64 executable installer" for 64-bit computers or "Download Windows x86 executable installer" for 32-bit computers. Run the installer and complete the installation.

IMPORTANT: make sure the box that says "Add Python 3.X to PATH" is checked, otherwise you may not be able to use the python/python3 command in the command prompt.

To check if pip3 is installed on the computer, open command prompt and type either of the following:
```
pip --version
pip3 --version
```
3. Install needed packages, depending on what model and frequency source you're using.
If you're going to use the Gulordava model (recommended):
```
pip3 install nltk
pip3 install torch===1.2.0 torchvision===0.4.0 -f https://download.pytorch.org/whl/torch_stable.html
```
The command for downloading torch depends on the versions you're using and going to install, look here for more details: https://pytorch.org/get-started/locally/.
If you're going to use the Jozefowicz model (called one_b in the code):
```
pip3 install tensorflow
```
(TODO: continue)
### Linux
1. Download the files by going to <https://github.com/vboyce/Maze>, clicking the green "Clone or Download" button, and selecting Download Zip. Once the zip file downloads, extract the maze_automate folder to the desired location. 
2. Install python3 and pip3 (copy/paste the shown commands into terminal/command line one by one, when prompted, type your password). 
```
sudo apt-get install python3
sudo apt update
sudo apt-get install python3-pip
```
3. Install needed packages, depending on what model and frequency source you're using.
If you're going to use the Gulordava model (recommended):
```
pip3 install nltk
pip3 install torch
```
If you're going to use the Jozefowicz model (called one_b in the code):
```
pip3 install tensorflow
```
If you're going to use [wordfreq](https://pypi.org/project/wordfreq/) for word frequencies:
```
pip3 install wordfreq
```
4. Make commands executable
Navigate into the maze_automate folder (command will differ depending on where you put the folder; use cd to move into a folder and ls to see the contents)
Example
```
cd Research/Maze/maze_automate
```
Make files exectutable
```
chmod +x set_up.py
chmod +x automate.py
```
5. Download model files and complete installation
From the maze_automate directory, run the appropriate command.
For Gulordava model only:
```
./set_up.py
```
For Jozefowicz model only:
```
./set_up.py --model one_b
```
For both models:
```
./set_up.py -- model both
```
If you plan on using wordfreq, add "--freq wordfreq" to the above command, i.e. for Gulordava model and wordfreq, you'd run
```
./set_up.py --freq wordfreq
```
6. Do a test run of distractor automation
test_input.txt contains a few sample sentences; replace output_location.txt with the name of the file to write test Maze materials to. 

To test Gulordava model
```
./automate.py test_input.txt output_location.txt
```
To test Jozefowicz model
```
./automate.py test_input.txt output_location.txt --model one_b
```
To test with wordfreq, add "--freq wordfreq" to the end of the above command. 

This may take a few minutes to run, but when it finishes you can check that the output file contains Maze materials for the input file.

## Basic Usage

### Set up a materials file
See test_input.txt for a sample. Materials should be in semi-colon delimited format. 
 - Column 1: condition. This is not used at all for distractor generation, but is copied to output. For ibex format output, this is treated as the "condition"/group. Good to use to indicate practice/filler/which type of critical item.
 - Column 2: item number. Sentences with the same item number will recieve the same sequence of distractors (and need to be the same length). 
 - Column 3: The good sentence. 
 
### Run
This can be computationally expensive to run, especially using the Jozefowicz model. If you have access to a computational cluster, we recommend using that. Otherwise, plan on running this overnight, or some other time when you don't need your laptop for a few hours. For testing, running a few sentences on a laptop should work okay. (Time is roughly linear in number of sentences, so you can guess how long a full set of materials will take by running a few sentences as a test and then multiplying.)

From inside maze_automate, in a terminal run

```
./automate.py test_input.txt output_location.txt
```

You can see the argument options with 
```
./automate.py -h
```
Arguments:
 - input (required) -- file with materials
 - output (required) -- file to write output to
 - model (default: gulordava) --  which model to use: gulordava or one_b 
 - freq (default: ngrams) -- which source to use for word frequency info: ngrams or wordfreq 
 - format (default: basic) -- which format to use for the output: basic or ibex 

Example usage: to run using the one_b model, with wordfreq frequency and ibex output format, you'd run
```
./automate.py test_input.txt output_location.txt --model one_b --freq wordfreq --format ibex
```

Advice on arguments:
 - model: Use one you did set-up for. (If you're just trying it out, we recommend Gulordava.)
 - freq: Ngrams using frequency information extracted from Google ngrams and was used for the Maze Made Easy experiments, so it's been tested. However, it cannot handle OOV words in materials at all. Wordfreq uses <https://pypi.org/project/wordfreq/>, which is robust to OOV words. Wordfreq requires that [wordfreq](https://pypi.org/project/wordfreq/) be installed. Each has some idiosyncratic biases based on the corpora they were trained on.
 - format: If you're going to run the experiments using Ibex, use ibex format, which is ready to be copied into the items section of a Ibex data file. If you will be checking materials or running materials with a different framework, use the basic format, which is semicolon delimited (like input format, but with an additional column for the distractors).

## Advanced options

### Banning words from being distractors

If the model is spitting out distractors that you don't want it to (i.e. they're not things you consider words, they're curses, they're historical words), you can add it to an exclude list. 

If you're using ngrams, add the bad words to exclude.txt and then in lexicon_generator.py add these lines to the bottom

>make_word_list()

>save_things()

Run lexicon_generator.py (python3 lexicon_generator.py), which will regenerate the distractor files. Then comment out the added lines in lexicon_generator. 

If you're using wordfreq, add the bad words to exclude_wf.txt, and then in lexicon_generator_wf.py add/uncomment these lines at the bottom

>make_word_list()

>check_dist("distractor_list.json")

Run lexicon_generator_wf.py (python3 lexicon_generator_wf.py), which will regenerate the distractor files. Then comment out the lines again. 

### Other lexicon considerations
Words in materials: The models handle OOV words reasonably well, but if you're writing new materials (as opposed to using/adapting materials from a previous study) you may want to choose words that are in the model's vocabulary. If you're using ngrams for frequency, all words must be in its vocabulary, or it won't run (you may want to try hyphenating/dehyphenating compound words to get into its vocabulary). If you're using wordfreq, this shouldn't be an issue, as it will assign a default low frequency to words it doesn't know (and will interpolate frequencies for words it thinks are multiple words). 

Distractor frequencies: In the ngrams model, you can manually assign new frequencies to words. The google ngrams corpus is generally reasonable about word frequencies, however when it parses things differently from how people do, there can be problems. In particular, it usually parses contractions as multiple words, so assigns unrealistically low frequencies to contractions. To fix this, we manually override contraction frequencies with the "contractions.csv" file. If you need to fix frequencies with other words, edit contractions.csv to add new words and floor log base 2 estimates of their occurance. Use get_freq to look up frequencies of some words for a baseline, and then compare their frequencies in another source to those of words you're fixing, and do some guessing or interpolation. Contraction frequencies come from google ngrams viewer. After you've made changes, run save_things to regenerate files. 
There isn't a provided way of altering distractor frequencies using wordfreq. 

Changing length/freq bins: Both frequency models bin distractors into length and frequency bins, and then use these lists as the distractor sources for matching good words. If you want to adjust these bins, with ngrams, edit the code in make_lexicon (in lexicon_generator.py), then run save_things. If you adjust length binning, also change the corresponding code in helper.py. For wordfreq, edit the code in lexicon_generator_wf, then uncomment and run the bottom lines. Also adjust the corresponding code in helper_wf.py. 

### Changing surprisal thresholds
Distractor word selection for either model is set to try 100 words, and choose either the first word with surprisal of 21 or higher or none of the 100 words have surprisal of 21 or higher, the word with the highest. These values can be changed in the function  do_sentence_set of one_b.py, one_b_wf.py, gulordava.py or gulordava_wf.py, as appropriate (wf = wordfreq version). 
