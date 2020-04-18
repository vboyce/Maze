Assorted unclassified maze notes to turn into the github pages:

# Introduction to the Maze task

Depending on where you're coming from, you may be wondering what this task even is. The easiest way to explain is to give an example instead. (Note that results from this sample are not actually analysed in any way.)

TODO: embed/link to an ibex maze instance
TODO: 

The Maze task is a word by word reading task, where the dependent measure is how long it takes to select the next word. Traditionally, the non-correct words (henceforth called distractors) were written by hand (see for instance TODO traditional maze papers). Usually they were real words that were chosen to fit poorly in the context (Grammatical maze), but nonce words have also been used (Lexical maze). 

Here we attempt to create Maze materials with real word distractors with much less effort by using language models to select the distractors. We take some list of potential distractors (i.e. a long list of words), take a subset that correspond with the correct word(s) in some way (for instance, similar length and unigram frequency), and then from that, pick a distractor to use that is high surprisal in the given position according to some language model. We do this for every word in the materials, and there we are.

The ideal is that it's always obvious which word fits in the context and which does not; we do not meet this ideal, but we do get close enough to get useful results anyway. However, we're still working to figure out if better models and parameter tweaks will get us closer to the ideal more often. 

If you care about having better materials, you may want to use A-maze as a starting point and then hand check and edit the places where distractors fall short. This is time consuming (which is why I personally just use the auto-generated materials and deal), but it's still easier than writing distractors entirely from scratch. 

For a much longer discussion of A-maze, there's a paper. (Note that the implementation has improved since then, so some of the technical details have changed, but overall principles and theory still hold.) TODO: link to paper

# Why use A-maze?

There are many cases where one may want reading/reaction time data, and Maze seems more desirable than either SPR or eye-tracking. One place this is likely to be true is running web-based experiments where SPR data can be very noisy. Maze is relatively rarely used, and A-maze is new, so we don't have a good sense of how good it is. As more experiments are done, we'll collectively come to a better understanding of what A-maze is good (or not good) for in terms of effects. 

In terms of why use A-maze over G-maze or L-maze, we find that L-maze doesn't show as strong effects, and I at least am far too lazy to write G-maze materials. 

# Recommended settings

# An argument in favor of redo mode 


Under the usual Maze task, as soon as you make a mistake the sentence terminates, and you move onto the next item. 

The first time we ran Maze experiments, we were trying to just automate distractors and otherwise stay close to what the task was, so we also did this. However, we then started thinking about how it might be nice to use this task, on longer items such as the Natural Stories corpus. That would be impossible because the stories were long, and no one would be able to get through them mistake-free. 

So, how to handle mistakes? We needed people to be able to continue the sentence somehow which means they needed to have the context, so they needed to see the correct word to include. Thus, I wrote a version where mistakes were met by an error message, but you would correct your mistake (by hitting the other button) and move on. 

Having collected some data using this method, I know think we should just always use this method.

First of all, this gives us more correct error rates because all participants who finish the experiment have seen the whole thing. We don't have the data censored by the mistakes. One obvious thing we see here is that (at least running on mturk), there appear to be two subpopulations -- those who try and those who randomly guess, with noticeably different error rates and RTs. Now, even if you're only going to use pre-mistake data, having the rest of the data makes it easier to figure out error rates (and potentially exclude participants) and to tell if there were issues with distractors, even late in the sentence (because you still have everyone's reading data there).

Second, it probably makes for a better user experience. I'm guessing here, but it may make mistakes (due to bad distractors or misclicking when you didn't mean to) seem less unfair, because you get to "fix" them and continue. 

Third, if this past-a-mistake data is useable, then there's more data; and for long items, potentially a lot more data. For items that are long, such as multi-sentence vignettes, we're almost certainly okay using data that is 10 words past the last mistake. It's not obvious what the buffer around mistakes should be (maybe the next couple words are less reliable and we should do some trimming?), but we can try to look at that and determine an empirically-based recommendation.

When in redo mode, the recorded RT is the RT to first push, so if they got it wrong, it's the time it took for that push. How many additional pushes and ms it takes until they press the correct button is not recorded.

# More redo mode thoughts

What do mistakes signify?

In some sense, mistakes could be coming from any of about 3 sources.
 1. The participant screwed up, and meant to hit the other button. (Hand mind coordination is hard sometimes.)
 2. The distractor was totally plausible. (Model did a bad job at this task) Note that this could be happening even when the distractor isn't as good as the good word, but when it's good enough to be reasonable (so semantically and syntactically plausible, even if not as predictable.)
 3. The participant was not paying enough attention; they were trying to do the task quickly, or they got distracted. 

We can get rid of a lot of the 3 mistakes by throwing out bad participants. There will still be the "got distracted" moments in otherwise attentive participants. 

How do we determine how good comprehension is? Could ask participants to type what they recall, or use comprehension questions. Issue with comprehension questions is they may query word level, which might be pretty remembered, versus syntactic structure.

We want to control out annoying RT effects and "still thinking about that last mistake" would count -- unclear how to detect this, although we could margin of 5 words or something I'd believe it gone. Arbitrary, but so is a lot of this. 

We also want some amount of comprehension control, and it's unclear what that's like for maze generally or with mistake continuing in particular. 

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


