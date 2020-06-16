---
layout: default
---


# Parameters

In addition to the input and output file locations, the program also gets a list of parameters from a parameters file. By default, it uses `params.txt`, but you can specify another file to change parameter values.

A parameter file wil look something like this.
```
#These are required
min_delta: 10
min_abs: 25
num_to_test: 200
#These are not required, but if they aren't here you get the defaults
dictionary_loc: "wordfreq_distractor"
dictionary_class: "wordfreq_English_dict"
threshold_loc: "wordfreq_distractor"
threshold_name: "get_thresholds"
model_loc: "gulordava"
model_class: "gulordava_model"
exclude_words: "exclude.txt"
include_words: "gulordava_data/vocab.txt"
max_repeat: 0
```
Three parameters control how hard the program to find good distractors.
 - min_delta is how much *more* surprising the distractors should be than the correct words (in bits)
 - min_abs is how surprising the distractors should be (in bits)
 - num_to_test is how many potential distractors the program tries (for one position in a sentence) before it gives up and returns the best so far. 

In general, high values should yield more surprising distractors, but we don't know how accurate surprisal values are, so raising them too high may end up just selecting for noise.

Max_repeat also effects what distractors are returned. Distractors never repeat within the same sentence, but by default, they can repeat across different items. If you don't want repeats, or if you find that some words are coming up as distractors too often, you can set max_repeat to a positive integer and no distractor will appear more than that number of times in the entire set of materials. Setting max_repeat to 0 (the default) means that no limit is applied. Note: this is a new feature, and we don't have any recommendations about what you might want to set it to. Setting it too high relative to the length of your materials and other parameters may result in worse distractors for sentences later in your materials. 

Other parameters tell the program what models and vocabulary sources to use and where to find them.
 - dictionary_loc and dictionary_class specify what possible distractors are
 - threshold_loc and threshold_name specify how to find what potential distractors to try for what correct words
 - model_loc and model_class specify what model to use to get surprisals

The next two parameters control what the pool of potential distractor words is:
 - exclude_words is a list of words that may not be used as distractors. So, if you see words getting used that you don't want, add them to this list (one word per line). For instance, you may want to ban curse words, abbreviations, or words no longer in common usage.
 - include_words allows only words on this list to be used as distractors. Here, it's set as the model's vocabulary, which means distractors are pre-filtered to be words the model knows (and not ones it treats as unknown).
 


## Parameter options

Available models, thresholds, and distractor dictionaries are currently limited. Include and exclude lists are recommendations, you may want more restricted word lists for some use cases. 

For the English Gulordava model, use:

```
dictionary_loc: "wordfreq_distractor"
dictionary_class: "wordfreq_English_dict"
threshold_loc: "wordfreq_distractor"
threshold_name: "get_thresholds"
model_loc: "gulordava"
model_class: "gulordava_model"
exclude_words: "exclude.txt"
include_words: "gulordava_data/vocab.txt"
```

For the French model, use:
```
dictionary_loc: "wordfreq_distractor"
dictionary_class: "wordfreq_French_dict"
threshold_loc: "wordfreq_distractor"
threshold_name: "get_thresholds"
model_loc: "french"
model_class: "french_model"
include_words: "french_data/frwac_vocab.txt"
```
