# French A-maze

This repo contains code for generating A-maze style distractors for French materials. It expects the French LSTM model used in [Represention of Constituents in Neural Language Models: Coordination Phrase as a Case Study](https://arxiv.org/abs/1909.04625v1), linked from [their github repo](https://github.com/cpllab/rnn_psycholing_coordination). 

This is a modification of the autogeneration of Maze materials; documention elsewhere in this repo may be helful. It is intended to generate materials to be run using [Ibex-with-Maze](https://github.com/vboyce/Ibex-with-Maze). 

#Set-up
Copy the model file (model_frwac.pt) into this folder.
Make sure you have pytorch and wordfreq modules installed. 

#Usage
Make automate_fr.py executable (chmod +x) or run using python3. It takes two mandatory arguments, an input file location and an output location. There's also an optional flag --format ; set this to "ibex" to get ibex ready output or "basic" to get semi-colon-delimited output. 

Input file should be formatted as per examples.txt, in semi-colon separated columns, first column is a label (which will get copied, but otherwise ignored), second column is an item number (sentences with the same item number must be the same length and will get the same word-by-word distractors), third column is the target sentence. 

#Files:
 - automate_fr.py is a wrapper that handles input/output and calls french.py
 - french.py calls the model and does the actual distractor generation process
 - distractor_list.json is a dictionary of potential distractors by length and frequency (created by lexicon_generator.py, used by helper.py)
 - exclude.txt is used by lexicon_generator to hand exclude words from the distractor inventory
 - examples.txt is a sample input
 - frwac_dicts.json is the model's dictionary
 - helper.py has code for looking up distractors used by french.py
 - lexicon_generator.py creates the distractor word list
 - model.py is something for the model
 - model_frwac.pt is the saved model checkpoint (needs to be copied in)
 - utils.py deal with the model's dictionary object
 - word_list.json is used by lexicon_generator
 - words.fr.txt is used by lexicon_generator
 
