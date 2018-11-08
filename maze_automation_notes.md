
# Overview of process so far

## Generating word lists

To generate length and frequency matched 'neighbors' for words I'm using google unigram corpora. I sum over all the years for each word and also sum over permutations of the word (_NOUN etc endings are discarded and than plurality wins). This is good for handling start of sentence capitilization, and also proper names. 'Words' that that have charcters other than apostrophe, hyphen, and letters are discarded. Additionally, words that occur less than 2^13 times (after summing over different forms) are discarded. 

Then, I create two dictionaries one for word --> unigram freq (floor(log2(# of occurances)), and one for (word length, unigram freq)--> list of words. Words of length less than 3 are mapped to length 3, words of length greater than 15 are mapped to length 15, and words of frequency greater than 25 are mapped to 25 to ensure decent neighborhood population.

Using these two we can then go from a word, to other words with the same length and unigram frequency. 

[ ] list of words should contain "real words" (as defined by some dictionary) that are lowercase, punctuation free words. (May also have to recheck binning after this.)

## Pre-processing sentences, finding alternates
   
Given an input file with one sentence per line, we take each word in each sentence (taking words as units between whitespace) remove end punctuation and look up some length and frequency matched alternates. Then we randomly choose some number of the alternates (20) to set off to the surprisal calculator.

For efficiency, we want to load and run the model as little as possible, so we compile an object with everything needed to run, and then send it to each of the models. 

## At the models

We currently are set up to use two models -- the Gulardova model and the Google One Billion model. In each model, we get surprisal values for each good word, each alternate, and 5 suggested words for each good word (i.e. run language model to predict next word 5 times). Unknowns are recorded as having surprisal -1 (to mark that they are unknown). 

Sentences are split into words using .split() (so words correspond to alternates), but then they are tokenized using an nltk tokenizer so that the model can have tokens. Thus, surprisal values for a good word are really surprisals for its first token. 

The model currently is run to return all the results so they can be printed and thought about. 

[ ] Find a better tokenizer choice for google one b
[ ] Refactor things so it's easier to plug in any model
[ ] Set them up to run on gpu
[ ] Algorithm for selecting alternate.
[ ] Apply matching case, end punctuation to chosen alternate
[ ] San check that the models are doing what we think they are

## After the model

Right now, do decisions are made, the model just returns a giant pile of surprisal values and such, and then they are neatly printed. 

[ ] (Post algorithm) Print a nice maze-ready file (or something close to it)

## Miscellanous wish list items

[ ] Cleaner code with classes, methods, readable code and documentation
[ ] Command line runnable with options
[ ] Minimal pair handling


