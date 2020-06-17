---
layout: default
---

# Parameter considerations: understanding the available knobs

Our goal is to get distractors that are individually highly infelicitous in context, but otherwise not easily distinguishable from the correct words. That is, we want to avoid there being obvious effective heuristics for guessing the correct word without processing the sentence. 

Unfortunately, the knobs we have don't include one for distractor quality. Instead, we have to try to balance a few considerations to achieve that. 

## The available knobs 

The parameters that trade off with each other are:
- min_delta
- min_abs
- num_to_test 
- max_repeat 

In general raising the minimums (min_delta and min_absolute) should increase the quality of distractors; although depending on the accuracy of the surprisal measures at approximating human judgments, there may be diminishing returns. If the minimums are high and num_to_test is relatively low, the algorithm will frequently return distractors that were the highest it saw, but are less than the minimum. If this seems to be happening a lot, increasing num_to_test may lead to higher surprisal distractors.

Depending on the relative values of min_delta and min_abs, one may matter more than the other. If min_abs is large, it may generally be larger than min_delta plus the real world surprisal, so changing min_delta small amounts may not make a difference. I try to balance them so distractors are high surprisal even when the real word is highly predictable (i.e. surprisal of 1), but to also try for an extra surprising word if the real word is also surprising (i.e. on the second word of a sentence). 

However, there's a reason to avoid just increasing all of these values. We don't want to overoptimize because the underlying distributions aren't perfect, and we don't want to be selecting for the noise and error between the available data and human judgments. For instance, some words may have listed frequencies that are higher that we'd perceive them as having due to quirks of the frequency corpora. This may correlate with them being high surprisal a lot of the time (because frequency and surprisal correlate), but they're not actually superior distractors. Similarly, there may be words where the models surprisal and human surprisal are not well-aligned, and the model generally assigns them high surprisal (moreso than humans would). If we increase the minimums and num_to_test too much, we're going to be getting these outlier distractors more, which doesn't help quality.

Thus, we want to increase the values while the gives better returns, but not beyond it to the point where it no longer helps and may start returning more junk. (This is all intuition/anecdotal, I have not done a systematic grid search on these values to see what happens.)

## Other considerations

In addition to wanting generally surprising distractors, I also want to avoid distractors that might look "weird" and might confuse or annoy participants, and so I apply additional hard restrictions on distractors. This is why I prevent swear words and abbreviations from appearing using the distractor exclude list. 

I was embarassed when I found out (from participant feedback) that for one word position, the distractor and correct word were the same, and so participants were stuck with a choice between between "Sticky" and "Sticky". The distractor generation process now explicitly prevents distractors being the same as the correct word.

Another consideration is not wanting the same distractor to appear consecutively, which is why distractors can't reappear within the same sentence. 

There's now a parameter for decreasing repeat distractor across an entire material set, by setting a hard maximum on the number of times a distractor can occur. Setting max_repeat too low relative to the length of the materials may decrease distractor quality towards the end of the materials (if all the better distractor options were already used). This is especially true if num_to_test is low, as that number are distractor options are selected and then ones that have already appeared are eliminated. 

## What I use

For recent experiments, I've been setting min_delta to 10, min_abs to 25, and num_to_test to 200. I haven't been limiting distractor repeats between sentences. I fairly often get distractors returned that do not meet the surprisal limit, but they tend to be reasonably high surprisal regardless. 
