---
layout: default
---

# What is A-maze?

## Demonstration

The easiest way to explain the method is to demonstrate instead; so try out the embedded [demo](http://syntaxgym.org:666/experiment.html) below. (Note that results from this sample are not analysed in any way.) 

<iframe src="http://syntaxgym.org:666/experiment.html" width="710" height="400" style="border:2px solid black;"></iframe>
<br>
## Explanation

The Maze task is a word by word reading task where a participant sees two words at at time and must select the correct word to continue. The dependent measure is the time to press the button. Traditionally, the non-correct words (henceforth called distractors) were written by hand. Usually they were real words that were chosen to fit poorly in the context, but nonce words have also been used. For more on the previous uses of the Maze task, see for instance [Forster, Guerrera, and Elliot, 2009](https://www.researchgate.net/profile/Kenneth_Forster/publication/23964016_The_maze_task_Measuring_forced_incremental_sentence_processing_time/links/0c960528e5bae4cf4b000000/The-maze-task-Measuring-forced-incremental-sentence-processing-time.pdf) and [Witzel, Witzel, and Forster, 2012](https://www.researchgate.net/profile/Jeffrey_Witzel/publication/51719334_Comparisons_of_online_reading_paradigms_Eye_tracking_moving-window_and_maze/links/556c4f7208aeab7772218886/Comparisons-of-online-reading-paradigms-Eye-tracking-moving-window-and-maze.pdf)). 

<img src="{{site.url}}/assets/maze_diagram.jpg" width="300" style="display:block;margin-left:auto;margin-right:auto" alt="diagram of Maze task"/>

Here we attempt to create Maze materials that mimic the properties of hand-written maze materials without the effort, which we call A-maze (short for Auto-maze). To do this, we use language models from Natural Language Processing to select distractors that are likely to be a poor continuation to the sentence so far. We take some list of potential distractors (i.e. a long list of words), take a subset that correspond with the correct word(s) in some way (for instance, similar length and unigram frequency), and then pick a distractor from that subset that is high surprisal (i.e. low probability) in that position according to some language model. We do this for every word in the materials. 

Ideally in a Maze task it's always obvious which word fits in the context and which does not. With A-maze we do not meet this ideal, but we do get close enough to get useful results anyway. However, using better language models or better parameter choices may get us closer to this ideal.

For a much more involved discussion of A-maze, please read [Boyce, Futrell, and Levy, 2020](https://psyarxiv.com/b7nqd/). Note that the implementation of A-maze has been improved since what is described in the paper; the theory and basic ideas hold true, some of the limitations less so. 

