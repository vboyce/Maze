
# Overview of process so far

## Generating word lists

To generate length and frequency matched 'neighbors' for words I'm using google unigram corpora. I sum over all the years for each word and also sum over permutations of the word (_NOUN etc endings are discarded and than plurality wins). This is good for handling start of sentence capitilization, and also proper names. 'Words' that that have charcters other than apostrophe, hyphen, and letters are discarded. Additionally, words that occur less than 2^13 times (after summing over different forms) are discarded. 

Then, I create two dictionaries one for word --> unigram freq (floor(log2(# of occurances)), and one for (word length, unigram freq)--> list of words. Words of length less than 3 are mapped to length 3, words of length greater than 15 are mapped to length 15, and words of frequency greater than 25 are mapped to 25 to ensure decent neighborhood population.

Only words that are all lower case, occur in a provided dictionary (words.txt is a copy of the dictionary provided on unix systems), and are not in an exclude list (exclude.txt, add not-actual words here) are put in the lists of works by length and frequency. 

Using these two we can then go from a word, to other words with the same length and unigram frequency. 

[x] list of words should contain "real words" (as defined by some dictionary) that are lowercase, punctuation free words. (May also have to recheck binning after this.)

## Input
   
Input is a csv file in three columns:  
 - 1st column is any information that should be kept and repeated in the output (maybe labels like "filler", or any other info that should stay attatched to the sentence)
 - 2nd column is an item number. Sentences with the same item number must be the same length in words and will recieve the same fillers. 
 - 3rd column is a sentence 

[ ] Change input stuff so we can handle not one-to-one word matches within items (maybe relevant for x tense cases?)

## Options
Currently, things can be run either with the Gulardova model or the Google One Billion model. Code for interfacing with each is parallel (and often repeated) because of slight differences in what objects they need passed around. 

The user gets to set a desired surprisal level (in bits) and a max number of alternates to try per spot. 

## Workflow

 - Input files are parsed by item number into a set of sentence groups
 - For each sentence group, for each spot in the sentence, we run language models for all the sentences up to that point, find a list of alternates for the next spot (matching average of length and frequency for the real continuation words), and check these words for surprisals in the language models. The first alternate word that exceeds the surprisal minimum for all sentences is used; if the max number of alternates to try (or all alternates provided) are tried, the word with best surprisal is returned. Alternates are processed to match capitalization and end punctuation with the good word. 
 - Output is a csv file similar to input, but with an additional column with sentence format of alternates (First word alternate is always x-x-x) 
Given an input file with one sentence per line, we take each word in each sentence (taking words as units between whitespace) remove end punctuation and look up some length and frequency matched alternates. Then we randomly choose some number of the alternates (20) to set off to the surprisal calculator.


[ ] Find a better tokenizer choice for google one b  
[x] Refactor things so it's easier to plug in any model  
[ ] Set them up to run on gpu  
[x] Algorithm for selecting alternate.  
[x] Apply matching case, end punctuation to chosen alternate  
[ ] San check that the models are doing what we think they are  
[ ] Output something better suited for maze? (or add a function to convert output --> maze input)

## Miscellanous wish list items

[ ] Cleaner code  
[ ] Command line runnable with options  
[ ] More generalized minimal pair handling  


