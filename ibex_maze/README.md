# Implementation of Maze for Ibex

## How to use

* Get a copy of Ibex (download from https://github.com/addrummond/ibex). 
* Add Maze.css and MazeSeparator.css files to the css_includes folder and Maze.js and MazeSeparator.js files to the js_includes folder. 
* You can test out the maze task by putting sample.js in the data_includes folder (remove anything else from that folder) and running (to test it out on your own computer, run "python server.py" from ibex/www -- experiment will be on localhost:3000). 

## Options

If you're building maze materials automatically using the scripts in maze_automate, you can get those materials in ibex-format, and just copy those lines into the items list of a ibex experiment file. 

If you're not, these are the available arguments and specifications. 

### Options for Maze: 
* s: Required. The correct sentence, either as a string or an array of words/chunks (same format as for spr). Usually starts with "The"
* a: Required. The alternative (incorrect) options. Can be either a string or an array of words/chunks, needs to have the same number of words/chunks as s. Usually starts with "x-x-x". 
* order: An array of 0's and 1's, the same length as s. Indicates whether the correct answer should be the left (0) or right (1) of the two options. If unspecified, will be 0 followed by a pseudorandom order of 0s and 1s (this constrains the first pair to be "The x-x-x" followed by random). Note: the default options means that different participants will see different orders. If you want them to all see the same order, you should specify. 

### Passing results to next item:
When a participant makes an incorrect selection, maze will record the time it took them to do so, but then it will stop that sentence, and pass "failed" to the next element. It is recommended to use "followEachWith" for maze items to follow each with a separator saying whether it was correct or not, so participants know when a new sentence is starting. 

Maze also displays a count of words gotten right so far. If you use the normal separator, the count will reset to 0 at the beginning of each item. If you want the count to be cumulative, you need to use MazeSeparator (.css and .js files included) to separate. All items that intervene between Maze tasks must contain the lines below for cumulative counting to work. 
> var x = this.utils.getValueFromPreviousElement("counter");

> if (x) this.utils.setValueForNextElement("counter",x);

## Result columns: (first seven are same as for other Ibex modules)
* 8.Word number: Starting at 0 for the first (no-real-choice) word.
* 9.Word: The text of the correct word.
* 10.Alternative: The text of the incorrect choice.
* 11.Word on (0=left, 1=right): Either 0 or 1 to indicate which side of the screen the correct word was displayed on. 
* 12.Correct: "yes" or "no" depending on whether the participant answered correctly. Note that "no" will be shown for words the participant did not see (i.e. words after the one they got wrong). 
* 13.Reading time: in ms. Reading time is provided for all words a participant saw, but the 0-word reading time is assessed differently (and so may not be comparable with other words in the sentence). Reading times are given for the word a participant gets wrong. "None" is used for words a participant did not see. 
* 14.Sentence. Text of the entire correct sentence. 
