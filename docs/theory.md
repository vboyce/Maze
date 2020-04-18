---
layout: default
---

The basic idea of A-maze is that given some experimental materials we generate a distractor word for each word in the materials, such that in the Maze task (sequential forced choices between the correct word and the distractor), participants can choose correctly, but with reaction time reflecting something meaningful about processing difficulty. 

Unpacking the details of various of the parts above gives us some desiderata, and gets us closer to what we need to do this. 

# Desiderata
- Experimental materials: We assume these are a set of sentences, which might have substantial structure. They might also contain just about any word and may contain low frequency constructions, perhaps even constructions that are not agreed-upon parts of the language. Ideally, we would not place constraints on what can occur in materials, although in many cases, experimental materials could be written or tweaked to use a restricted set of language. 

- Distractor word: While we call them "distractors", the foils really should not be distracting, and should be rather bland. That is, they should be easily identifiable as words, and not distract participants with their weirdness, unknownness, or frequent repetition. At the same time, at a surface level, they should "match" the real words, so that the only way to pick out the correct word involves some of that processing we're interested in. There should not be easy to identify heuristics for distinguishing the distractors. 

- "Can choose correctly": On the other hand, we do want the distractors to be clearly worse than the correct word given the sentence context. Otherwise, participants might get frustrated, and we don't get the data we want. 

- Something meaningful about processing difficulty: Critical items are likely to be in minimal pairs (or n-tuples), and it may be desirable to match distractors between words that represent minimal pairs for the analysis. This leads to wanting to be able to specify distractor match locations freely; however, many paradigms will want one of a few simpler types of matching (and so for ease of use, we'd like these common types to be easy to specify). 

# Some of the choices we made

To address the "matching" between distractors and correct words, we try to make them be similar in terms of length (in characters) and frequency (overall). We also match on capitalization and punctuation to the correct word, which means the distractors need to be okay in either/any case, which restricts to naturally lowercased words (aka, no proper nouns). 

There are less straightforward choices to be made in handling materials with unusual words, such as copious abbreviations or numerals, and we're still working on what will look reasonable. 

## Trade-offs between match, search-time, and badness
Assuming a perfect language model, it might make sense to optomize for the worst of a set of possible distractors. In our method, we generate a list of potential distractors (on length/frequency match) and then sample until we find one that meets the set surprisal thresholds or until we've tried a bunch and we back off and take the best so far. However, given imperfections of determining frequency and surprisal, optomizing would not only take longer, but it would also probably find exceptions -- the words where frequency was off or where the language model was confused. It also might find these consistently. 

Another constraint on the aesthetics of distractor words is that we'd like them to not appear to frequently. Not only does frequency perhaps imply some issues with the underlying generative models (frequency, language model), but it's going to bely what's going on if the same three letter word comes up frequently. 



# What you'd need for this process
One big reason to think about what is needed for A-maze is if you wanted to run A-maze in another language.

For this you'd need:
- a list of valid distractor words (computer dictionaries might be helpful, but also may need to be cut for things like abbreviations or swear words). In some languages, requiring that the distractor words consist only of characters from some list of valid characters may help. 
- a way of telling how bad/surprising a word is in a given context. This probably will be some sort of neural language model, which thus probably requires a large corpora of text to train on. 
- a way of choosing potential distractors. For instance, if you're trying to match by frequency, you'll need frequency data for the distractor words and correct words, and potentially a plan for what happens when the word is unknown. 

Other things to keep in mind:
How punctuation and capitilization work, and whether they should get matched. For instance, in English, we capitilize the distractor to match, but that wouldn't necessarily make sense for German. 
Depending on the tokenization scheme of the language model and how well it matches (or doesn't match) with word boundaries in the written language, there might be things to consider. It's recommended that distractor words be single tokens so that surprisal calculations are easier. 
(also need a plan for tokenization of lm)


