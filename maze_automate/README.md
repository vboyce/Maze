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
Make sure pip3 is updated to the latest version, which could be done using the following command:
```
python3 -m pip install --upgrade pip
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
If you're going to use [wordfreq](https://pypi.org/project/wordfreq/) for word frequencies:
```
pip3 install wordfreq
```
Continue step 4 in All Operating Systems.
### Mac OS X
1. Download the files by going to <https://github.com/vboyce/Maze>, clicking the green "Clone or Download" button, and selecting Download Zip. Once the zip file downloads, extract the maze_automate folder to the desired location. 
2. Install python3 and pip3 by going to https://www.python.org/downloads/mac-osx/ and selecting under Stable Releases > (latest Python 3 version) > "Download macOS 64-bit installer" for 64-bit computers or "Download macOS 64-bit/32-bit installer" for 32-bit computers. Run the installer and complete the installation.
To check if pip3 is installed on the computer, open command prompt and type the following:
```
pip3 --version
```
Make sure pip3 is updated to the latest version, which could be done using the following command:
```
python3 -m pip install --upgrade pip
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
If any dialog box pops up to install gcc, follow their instructions.
Continue step 4 in All Operating Systems.
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
Continue step 4 in All Operating Systems.
### All Operating Systems
4. Make commands executable
Navigate into the maze_automate folder (command will differ depending on where you put the folder; use cd to move into a folder and ls to see the contents)
Example
```
cd (where the repository is stored)/Maze/maze_automate
```
Make files exectutable
```
chmod +x set_up.py
chmod +x automate.py
```
5. Download model files and complete installation
From the maze_automate directory, run the appropriate command. For Windows, ignore the ```./``` part of the commands and use ```python3 ...``` instead.
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
If there is an error indicating that it cannot import wget, use the command ```pip3 install wget```.
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
Materials should be in semi-colon delimited format. The input format is as follows (see test_input.txt as an example):
>"[label for sentence set]"; [ID for sentence set]; [Sentence]; [Word order]

 - The label for sentence set (condition) is purely for ease of the researcher, to give an easy categorization of the sentence sets. Examples include "adverb_high" and "adverb_low". This is not used at all for distractor generation, but is copied to output. For ibex format output, this is treated as the "condition"/group. Good to use to indicate practice/filler/which type of critical item.
 - ID for sentence set (item number) is more important programmatically. The program will feed the sentences by increasing ID, and will group together the same IDs as belonging in the same set. The IDs can be any integer, for example 0, 1, 70 and 72.
 - The sentence follows. The format is plain text, capitalization allowed.
 - The word order is an optional part of the input format, telling the program which words to group together to generate the same distractor word. For example, the same word "filmed" appearing at different locations in each sentence may be given the same word ID so that the same distractor word is generated for the same word "filmed". An example would be 0 1 2 3 4 5, and 0 2 1 4 3 5.
 
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
 - input: location and name of the input file, for example test_input.txt
 - output: location and name of the output file, for example output_location.txt

Optional arguments:
 - ```--model```: choice of the model to be run on the sentences, choose between ```--model=gulordava``` (which is the default) and ```--model=one_b``` (which has not been refactored)
 - ```--freq```: choice of the frequency data to accompany the model, choose between ```--freq=ngrams``` (which is the default) and ```--freq=wordfreq```
 - ```--format```: output file format, choose between ```--format=ibex``` and ```--format=basic``` (which is the default; csv file)
 - ```--num_to_test```: number of words to test in the process of finding bad words, for example ```--num_to_test=100```
 - ```--min_abs```: absolute threshold of surprisal for a bad word, for example ```--min_abs=21``` (which is the default, meaning that we are aiming for bad words with at least a surprisal value of 21 throughout the whole process
 - ```--min_rel```: relative threshold of surprisal for a bad word to compare with the good word, for example ```--min_rel=5``` and ```--min_rel=-1``` (which is the default and indicates that relative threshold is not used)
 - ```--duplicate_words```, indicating whether duplicate words are allowed within a particular output sentence. The default value is false, and if the parameter is included as ```--duplicate_words```, then the value becomes true.
 - ```--matching```: choice of matching method to be used for each sentence in a sentence set, choose between ```--matching=index``` (which is the default), ```--matching=manual``` and ```--matching=auto```

Example usage:
To run using the one_b model, with wordfreq frequency and ibex output format, you'd run
```
./automate.py test_input.txt output_location.txt --model one_b --freq wordfreq --format ibex
```

### Note for threshold:
The following are example cases to demystify absolute threshold and relative threshold.

```--min_abs=21 --min_rel=-1```: The threshold of surprisal to find bad words is constantly at 21.

```--min_abs=21 --min_rel=5```: The threshold of surprisal to find bad words depends on each original word, and is whatever is more between 21 and (original word's surprisal + 5).

### Note for matching:
```--matching=index``` treats words at the same index as the same group and generates one bad word for the group of words. Each sentence in a set must have the same length. For example,
>This is sentence one.

>Then, the second sentence.

One bad word will be generated for [this, then], [is, the], [sentence, second], [one, sentence].


```--matching=manual``` treats words that are specified to have the same ID as the same group and generates one bad word for the group of words. Each sentence does not need to have the same length. The first words of the sentences must not match with words from elsewhere in the sentences. An example for this option is,
>This is sentence one. 0 1 2 3

>Then, the second sentence comes. 0 1 3 2 4

One bad word will be generated for 0:[this, then], 1:[is, the], 2:[sentence, sentence], 3:[one, second], 4:[comes].


```--matching=auto``` treats identical words as being in the same group and generates one bad word for the group of words. The first words of the sentences must not match with words from elsewhere in the sentences. An example for this option is,
>This is sentence one.

>That is the second sentence.

One bad word will be generated for [this], [that], [is, is], [the], [sentence, sentence], [one], [second].

### Advice on arguments:
 - model: Use one you did set-up for. (If you're just trying it out, we recommend Gulordava.)
 - freq: Ngrams using frequency information extracted from Google ngrams and was used for the Maze Made Easy experiments, so it's been tested. However, it cannot handle OOV words in materials at all. Wordfreq uses <https://pypi.org/project/wordfreq/>, which is robust to OOV words. Wordfreq requires that [wordfreq](https://pypi.org/project/wordfreq/) be installed. Each has some idiosyncratic biases based on the corpora they were trained on.
 - format: If you're going to run the experiments using Ibex, use ibex format, which is ready to be copied into the items section of a Ibex data file. If you will be checking materials or running materials with a different framework, use the basic format, which is semicolon delimited (like input format, but with an additional column for the distractors).

### Log format (printed on terminal):
While running maze_automate, the terminal will print on screen according to the following format:
```
Number of bad words to test = N
(not wordfreq) – prints if the model used is not wordfreq

(Good word ‘…’ unknown)
Minimum threshold = X
(Candidate bad word ‘…’ unknown)
(Couldn't meet surprisal target, returning with surprisal of Y)
```

### Output format (output_location.txt):
The output format depends on whether the user specifies ```--format=ibex``` or ```--format=basic```, however it generally follows the same format as the input.

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
