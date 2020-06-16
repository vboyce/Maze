---
layout: default
---

# Experimental pipeline for using A-maze

The pipeline for running an A-maze experiment is similar to running an SPR experiment. 

1. Create materials. You will need to source the sentences you'll be testing (and don't forget fillers, if appropriate). You should also source a few practice sentences, so participants can get used to the task before reading items you care about. 

2. Format materials into the maze input format as described [below](#formatting-materials).

3. Install A-maze generation following [these instructions](install.md). If you are using a model other than gulordava, you may need to install additional packages (run `./set_up.py -h` to see available models, and `./set_up.py --desired_model` to set-up the model). 

4. Run the materials. To run the materials, run `./distract.py input_file.txt output_file.txt`. Optionally append `-p parameter_file.txt` to specify a file with parameters and `--format ibex` to output in ibex format. See more on [parameters](parameters.md). 

5. Format your materials, and put them in the experimental setup. If you're running your experiment using Ibex, you can copy the maze output into the items list of a ibex experiment file. Add whatever other experimental parts you need (consent statement, instructions, comprehension questions, demographics, etc), and check that the experiment runs as desired. See [Ibex-with-Maze](ibex.md) for more on using Ibex for Maze experiments. 

6. Collect data.

7. Analyse results. See [a sample R script](experiments.md#analysing-results) for turning Ibex results files into rectangular data tables.

# Formatting materials

Maze accepts materials in a semicolon delimited format (like csv, but with semicolon as the special character that separates elements).

You should make it look like test_input.txt, as shown.
```
sample;1;The dog chased the cat around and around the house.
sample;2;The cat ran far, far away from the dog.
sub_rel;3;The cat who the dog scared hid in a box.;pre_1 pre_2 who art noun verb main_verb post_1 post_2 post_3
obj_rel;3;The dog who scared the cat sniffed around the couch.;pre_1 pre_2 who verb art noun main_verb post_1 post_2 post_3
```

1. The first column is a name for the type of sentence; the distractor generation process will ignore this, but copy it along to output (and it will become the condition label if you output in Ibex format). 

2. The second column is the item identifier (it doesn't need to be a number). Sentences with the same item identifier will get matched distractors. 

3. The third column is the sentence. 

4. The (optional) fourth column is the labels. This is used to tell the model which words in sentences with the same item identifier should get the same distractors. The model will just use them to match, so you whatever labels are easiest for you. The number of labels must match the number of words in the sentence. If labels are not given, the words will be labelled 1:n.   
This means there is no need to label sentences if they are the only one with that item identifier (ex. fillers). If there are multiple sentences with the same item identifier and they are not labelled, the first words will get the same distractor, the second words will get the same distractor, etc. (In some cases, this will be desirable.)  
If you want them to match up differently specify labels for the sentences. For instance, in the test_input sample above, _scared_ is always labelled as "verb"; if we were comparing RTs on verbs in object versus subject relative clauses, we'd be able to say that the distractors weren't a source of difference between conditions. (It's unclear if this actually matters, but the ability to control it is available.)

None of these fields need to be quoted (except if your have semicolons in your materials), but they can be. You may find it easier to put together and label your items in another program (R or a spreadsheet editor) and then save them to this format. 

# Guarantees and lack thereof

This code is offered as is; it's supposed to do a few things (assuming I didn't make coding errors) and it hopefully does some other things. 

Supposed to:
- not repeat distractors within an item identifier (this means that each distractor should appear at most once in any sentence; if you want to further limit distractor repeats see the max_repeats [parameter](parameters.md))
- not given any word itself as a distractor 

Hopefully:
- usually provides substantially infelicitious distractors (absolutely no guarantees that they will be "ungrammatical", but empirically they're usually bad enough that attentive participants can easily and accurately pick the correct word)


# Other notes

The Gulordava model runs fairly quickly; however, running language models is computationally intensive, so if you have access to a computational cluster, you may want to use that. Otherwise, just be prepared to have it run on your laptop for a bit. (You can always time it on 5 or 10 sentences before running a longer set of materials to get a guess on how long it will take.)

