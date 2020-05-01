# Autogenerating Maze materials

(See Section 3 of [Maze Made Easy](https://psyarxiv.com/b7nqd/) for the motivation behind this approach, schematics of how it works, and some advice for its use.)

This code takes experimental materials (sets of sentences, such as for SPR) and generates distractors words for each position, returning A-maze materials. Distractor words are guaranteed to be (roughly) length- and frequency-matched to the target word(s); they are also guaranteed to be high surprisal under the language model. This will often mean they are ungrammatical or otherwise obvious mismatches to the context, but it's not guaranteed. 

Please see [the github pages site](https://vboyce.github.io/Maze/) for information on how to install and use A-maze. 
