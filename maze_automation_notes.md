
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
| 23.97480583190918 | 26.46285057067871 | 23 | 27 | reporter  |admired |
 | 21.112266540527344 |  19.74556541442871 |  31 |  31 |  had | are |
 | 24.579774856567383 |  25.566600799560547 |  25 |  25 |  dinner | save |
 | 29.05268096923828 |  30.04982566833496 |  24 |  26 |  yesterday | myself |
 | 20.047908782958984 |  30.420507431030273 |  32 |  23 |  with | tank |
 | 33.25505065917969 |  24.00752067565918 |  35 |  28 |  the | go |
 | 25.288055419921875 |  25.235382080078125 |  23 |  28 |   baseball | take |
 | 22.89716148376465 |  23.90438461303711 |  24 |  22 |   player | pose |
 | 17.975175857543945 |  35.5666389465332 |  30 |  26 |   who | speak |
 | 12.99376106262207 |  20.013521194458008 |  22 |  27 |  Kevin | body |
 | 31.829620361328125 |  21.151525497436523 |  23 |  23 |  admired | guys |

Mostly, we see that surprisal/relative surprisal is not going to be a perfect measure (predicts that 'guys' better than 'admired'), so we're hoping that large enough numbers/differences really make things bad. 

Next, I tried arbitrarily choosing potential alternates and seeing what their surprisals were. Context, then first line is the 'good' word, then some alternates and their surprisals.

The   
['reporter', 23.97480583190918]    
['splendid', 24.90536117553711]  
['enjoying', 27.496967315673828]  
['deciding', 28.561344146728516]  
['drawings', 28.744977951049805]  
['mentally', 30.318307876586914]  
['pointing', 32.033897399902344]  
['fracture', 32.51325988769531]  
['paradise', 35.768348693847656]  
['depended', 39.373531341552734]  
['perceive', 42.75691604614258]  

The reporter   
 ['had', 21.112266540527344]  
 ['one', 17.91001319885254]  
 ['but', 22.197383880615234]  
 ['you', 22.89556884765625]  
['his', 23.668861389160156]   
 
 The reporter had   
 ['dinner', 24.579774856567383]  
['doctor', 20.653162002563477]  
['orders', 24.62776756286621]  
['broken', 26.547609329223633]  
['cities', 26.473920822143555]  
['stress', 27.845401763916016]  
['served', 30.01453971862793]  
['tables', 30.319805145263672]  
['unable', 32.349151611328125]  
['duties', 36.887237548828125]  
['edward', 44.53696823120117]  
 
 The reporter had dinner   
  ['yesterday', 29.05268096923828]  
  ['perceived', 23.652320861816406]  
  ['diversity', 23.320693969726562]  
  ['empirical', 26.086444854736328]  
  ['customers', 26.165138244628906]  
  ['directors', 28.52153205871582]  
  ['affection', 28.96552276611328]  
  ['libraries', 30.89655303955078]  
  ['measuring', 32.73731994628906]  
  ['witnesses', 33.15302658081055]  
  ['plaintiff', 38.271034240722656]  
  
 The reporter had dinner yesterday   
   ['with', 20.047908782958984]  
   ['that', 24.91154670715332]  
   
 The reporter had dinner yesterday with   
    ['the', 33.25505065917969]  
     
    
 The reporter had dinner yesterday with the   
 ['baseball', 25.288055419921875]  
? ['throwing', 26.92560577392578]  
o ['commands', 28.507186889648438]  
x ['symmetry', 29.419092178344727]  
? ['annually', 30.681936264038086]  
x ['efficacy', 32.58613586425781]  
x ['utilized', 33.989933013916016]  
o ['husbands', 33.302833557128906]  
o ['buddhist', 39.89736557006836]  
x ['receptor', 42.39029312133789]  
 
 The reporter had dinner yesterday with the baseball   
['player', 22.89716148376465]  
['deeper', 22.415802001953125]  
['smooth', 24.986736297607422]  
['topics', 26.370197296142578]  
['fruits', 27.864635467529297]  
['viewed', 27.16878890991211]  
['firmly', 29.291152954101562]  
['screen', 29.692142486572266]  
['strike', 32.393592834472656]  
['breath', 34.374359130859375]  
['miller', 36.802677154541016]  

    
The reporter had dinner yesterday with the baseball player   
['who', 17.975175857543945]  
['has', 18.126537322998047]  
['can', 19.33433723449707]  
['all', 21.970523834228516]  
['may', 23.42855453491211]  
['him', 24.559154510498047]  
['she', 25.349952697753906]  
['her', 26.464155197143555]  

     
The reporter had dinner yesterday with the baseball player who  
['Kevin', 12.99376106262207]  
['daddy', 28.464637756347656]  
['folds', 30.381877899169922]  
['creep', 31.83360481262207]  
['herbs', 32.085933685302734]  
['infra', 38.690589904785156]  
['dwelt', 39.07101821899414]  
['bless', 41.446083068847656]  
['sudan', 42.30971145629883]  
['ghana', 42.811729431152344]  
['digit', 48.42172622680664]  
      
The reporter had dinner yesterday with the baseball player who Kevin   
['admired', 31.829620361328125]  
['obscure', 23.41954231262207]  
['parking', 24.398550033569336]  
['plainly', 28.353910446166992]  
['license', 29.508159637451172]  
['outlook', 30.418350219726562]  
['trusted', 32.76241683959961]  
['relates', 35.003623962402344]  
['furnish', 37.430789947509766]  
['clauses', 41.0998420715332]  
['alabama', 49.8082275390625]  

This reveals a few things:
 1) some words (the, with) don't have enough neighbors under the current scheme. I need to adjust how words are being grouped to handle frequent short words better and will want a scheme for if none of the neighbors meet the badness criteria, where to look next (obvious options are the off-by-ones for either length or frequency). 
 2) As hinted at above, handling alternates in all lower case has issues because the language model deals with capitilization. There are certainly ways we could try to handle this, but I'm not sure any of them are good. 
 3) We should probably try a few different cut-off criteria on naive subjects to figure out what to use -- surprisal is not a great predictor of grammaticality judgments, so we're going to need a measure of 'is it obviously worse?', and I can't tell just by looking at them. (This also may suggest that this method of generating alternates may work better for some types of tasks than others (i.e. grammatical but semantically dubious good words are not going to fare well, is my guess.)
 4) Cutoff possibilities: I think I'm tempted to try 35 and 40 as cutoffs. My sense is that absolute may be better than relative, although we could also try >15 more than the good word. The reason to try relative is that if surprisal is substantially driven by overall frequency, we may not be able to find short/frequent words with high enough surprisal. What's the correlation (if any) between surprisal and unigram frequency? Is this something I should be worrying about? 
 
# Plan going forward
Aside from addressing the above issues, there are some things I need to figure out / write code for before we can generate enough to test things on other people. 
1) handling punctuation. Maze treats punctuation as attached to the previous word, but the language model wants it treated as its own word. This should be easy enough to code, but I will need to handle it. 
2) Running things on a machine with more computation. I assume the solution here is to learn how open mind works and get an account and use that for running > 1 sentence worth of alternate generation. 
3) Algorithm: I think for each word that needs a distractor, I should randomly permute its list of neighbors, and then go through that new list until I find a word that meets the cutoff criteria. If the end of the list is reached, have some rule for what list to try next. (This assumes the goal is one alternate / word, but it could be modified if we want backups.)

