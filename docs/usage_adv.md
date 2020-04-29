---
layout: default
---

# Structure of maze automation

This is written with the assumption that you might be trying to mess with things or add new modules to maze automation. 

Files and what they do:
- distract.py is the commandline interface, and just wraps main.py
- main.py: has function run_stuff that does everything 

- set_params.py reads in the parameter file
- input.py reads in the input file
- output.py writes output to delim or ibex format

- sentence_set.py: has classes Sentence, label, and Sentence_Set, handles a lot of the organizational heavy lifting

- distractor.py: has parent classes distractor and distractor_dict 
- wordfreq_distractor: has a general dictionary implementation that does length and frequency comparisons (and also also supplies related frequency and threshold functions); instantiated for English and French in two subclasses 


- lang_model.py: has parent class for language models
- gulordava.py: gulordava model subclass of lang_model
- french.py: french model subclass of lang_model

- utils: has arbitrary functions other files want

# Things you might want to mess with

Some obvious steps to mess with:
- The distractor word source and frequency information. It's unclear how good wordfreq is, and you could definitely create a new subclass of distractor_dict. It would also want corresponding frequency and threshold functions.
- Change matching process. Similarly, better or different methods of finding distractors to test could surely be designed. You'd just need to sub out the threshold function (and maybe the dictionary if you want a more interactive search/back-off procedure.)
- Change the language model. Just made something that behaves similarly to the parent class/gulordava model. This should approximately just work for models that tokenize at approximately the word level (modulo a few stray multi-token words, punctuation, etc) and return a distribution over next tokens. The key point is that these "next tokens" need to include lots of whole words. (So, no BPE models, at least for now.)
(Digression: It's probably possible to get this set up to deal with BPE models, but it would be non-trivial.)

# Adding other languages

It shouldn't be hard to set up Maze to work for non-English languages. The hard part is finding/making a good language model. As a proof-of-concept, a set-up for French maze is provided. 

The key things to consider are:
- Distractor words and frequencies -- for French, we use wordfreq, and only allow words in the model vocabulary; however, the exclude list hasn't been populated because my French isn't very good. Similar to with English, we use a regex to exclude words with numbers or punctuation, but for French we enumerate a list of acceptable accented characters.
- What features of distractors should be post-matched to correct words. (Depending on language, it may or may not be appropriate to match capitalization.)
- Interfacing with the language model. You may need to deal with tokenization. (the French model uses an lstm with similar architecture to the gulordava model, so the interfacing is similar.)

If you do fix bugs, add new features, or new languages; please submit pull requests! 
