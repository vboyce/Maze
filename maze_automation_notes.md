
# Overview of process so far

To generate length and frequency matched 'neighbors' for words I'm using google unigram corpora. I sum over all the years for each word and also sum over permuatations of the word (Foo, foo, foo_NOUN, etc. are all mapped to foo). This is good for handling start of sentence capitilization, not so good for proper names. 'Words' that that have charcters other than apostrophe, hyphen, and letters are discarded. Additionally, words that occur less than 2^13 times (after summing over different forms) are discarded. 

Then, I create two dictionaries one for word --> unigram freq (floor(log2(# of occurances)), and one for (word length, unigram freq)--> list of words. 

Using these two we can then go from a word, to other words with the same length and unigram frequency. 

Once we have these words, we can test their surprisal given the initial context (using the the 1 billion language model, tensorflow, and the code Richard sent me). 


# Playing around

I took one of the practice items ('The reporter had dinner yesterday with the baseball player Kevin admired.') from the maze task and have been using it for exploration.

What are the surprisal and frequencies of the words and alternates they used?

|good-surprisal |bad-surprisal | good-freq | bad-freq | good| bad |
| --- | --- | --- | --- | --- | --- |
| 23.97 |31.82  | 23 | 27 | reporter  |admired |
 | 8.03 | 10.22 |  31 |  31 |  had | are |
 | 11.53 | 19.80  |  25 |  25 |  dinner | save |
 | 9.81 | 16.43  |  24 |  26 |  yesterday | myself |
 | 1.27 | 23.23 |  32 |  23 |  with | tank |
 | 2.96 | 17.53  |  35 |  28 |  the | go |
 | 15.02 | 16.59  |  23 |  28 |   baseball | take |
 | 2.89 |  25.16 |  24 |  22 |   player | pose |
 | 3.73 | 19.93  |  30 |  26 |   who | speak |
 | 17.14 | 20.20 |  22 |  27 |  Kevin | body |
 | 16.30 |  21.20 |  23 |  23 |  admired | guys |



Next, I tried arbitrarily choosing potential alternates and seeing what their surprisals were. Context, then first line is the 'good' word with it's surprisal, then some alternates and their surprisals.

The   
|reporter | 23.97|
| --- | --- |
|vehicles | 24.62| 
|opposing | 26.16| 
|carriers | 26.85| 
|balanced | 27.66| 
|grateful | 29.22| 
|oriental | 30.99| 
|drainage | 32.43| 
|distress | 35.34| 
|withdraw | 38.71| 
|missouri | 40.01| 

The reporter   
 | had | 8.03|
| --- | --- |
|you | 8.90| 
|are | 10.22| 
|but | 10.30| 
|his | 11.86| 
|one | 12.11| 

 
 The reporter had   
 
 
 | dinner | 11.53|
| --- | --- |
|walked | 10.20|
|proved | 11.67 |
|served | 11.82| 
|credit | 16.87| 
|thirty | 18.05| 
|chance | 18.26| 
|reduce | 20.78| 
|seeing | 20.95| 
|agency | 21.42| 
|oxford | 28.41| 


 The reporter had dinner   
| yesterday | 9.81|
| --- | --- |
|occasions | 16.22| 
|furniture | 18.24| 
|currently | 18.99| 
|requiring | 19.95| 
|inventory | 20.42| 
|evidently | 20.52| 
|shoulders | 21.88| 
|proceeded | 23.83| 
|defendant | 25.58| 
|parameter | 28.26| 

  
 The reporter had dinner yesterday   
  
| with | 1.27|
| --- | --- |
|that | 8.87| 


 The reporter had dinner yesterday with   
  

| the | 2.96|
| --- | --- |

    
 The reporter had dinner yesterday with the   
| baseball | 15.02|
| --- | --- |
|defeated | 13.20| 
|discount | 18.59| 
|exterior | 19.41| 
|maritime | 20.01| 
|manifest | 20.26| 
|russians | 22.39| 
|avoiding | 23.10| 
|reversed | 23.47| 
|preceded | 24.27| 
|amounted | 27.17| 

 
 The reporter had dinner yesterday with the baseball   
| player | 2.89|
| --- | --- |
|paying | 16.31| 
|debate | 17.10| 
|threat | 17.53| 
|prison | 18.53| 
|domain | 19.39| 
|reveal | 20.12| 
|plasma | 21.78| 
|lowest | 22.85| 
|engage | 23.13| 
|tended | 25.45| 

The reporter had dinner yesterday with the baseball player   
| who | 3.73|
| --- | --- |
|she | 10.9| 
|all | 10.99| 
|has | 12.70| 
|her | 13.40| 
|him | 13.58| 
|may | 16.53| 

The reporter had dinner yesterday with the baseball player who  
| Kevin | 17.14|
| --- | --- |
|waved | 14.86|
|coats | 18.36|
|curse | 21.38|
|gloom | 27.62|
|optic | 28.58|
|karen | 29.51| 
|annie | 30.67|
|verbs | 30.68|
|piety | 31.91|
|psalm | 33.77|

The reporter had dinner yesterday with the baseball player who Kevin   

| admired | 16.30|
| --- | --- |
|crushed | 18.31|
|wrapped | 19.63|
|chances | 22.63|
|glasses | 24.35|
|minimal | 24.39|
|ongoing | 26.08|
|damages | 27.25|
|sheriff | 27.56|
|glucose | 32.25|
|peasant | 35.34|

This reveals a few things:
 1) some words (the, with) don't have enough neighbors under the current scheme. I need to adjust how words are being grouped so that more/all of the groups have enough members. I will also want a scheme for if none of the neighbors meet the badness criteria, where to look next (obvious options are the off-by-ones for either length or frequency). 
 2) As hinted at above, handling alternates in all lower case has issues because the language model deals with capitilization. There are certainly ways we could try to handle this, but I'm not sure any of them are good. One option is to give each word the majority capitilization pattern -- this should take care of names/places well? 
 3) We should probably try a few different cut-off criteria on naive subjects to figure out what to use. 
 4) Cutoff possibilities: Maybe go with a surprisal of at least 10 higher? 
 
# Plan going forward
Aside from addressing the above issues, there are some things I need to figure out / write code for before we can generate enough to test things on other people. 
1) handling punctuation. Maze treats punctuation as attached to the previous word, but the language model wants it treated as its own word. This should be easy enough to code, but I will need to handle it. 
2) Running things on a machine with more computation. I assume the solution here is to learn how open mind works and get an account and use that for running > 1 sentence worth of alternate generation. 
3) Algorithm: I think for each word that needs a distractor, I should randomly permute its list of neighbors, and then go through that new list until I find a word that meets the cutoff criteria. If the end of the list is reached, have some rule for what list to try next. (This assumes the goal is one alternate / word, but it could be modified if we want backups.)

