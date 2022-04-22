---
layout: default
---

# Implementation of Maze for Ibex

To run Maze experiments online, there is a custom Ibex module that runs the Maze task. It is an adaptation of the SPR module, and uses the same timing mechanism as SPR. For general information on using Ibex, please see user documentation at <https://github.com/addrummond/ibex/blob/master/docs/manual.md>.

The Ibex implementation is now kept in a separate repository from the A-maze implementation, although they are meant to work together.

## Setup

* Download [this respository](https://github.com/vboyce/Ibex-with-Maze) using the green "Clone or Download" button, and selecting Download zip. 
* You will need Python 2; you can install from <https://www.python.org/downloads/release/python-2714/>.
* You can test out the maze task by running the file *server.py* in the folder www/ using python 2. You can do this in a python application, or from in the terminal navigate to the www folder and run "python2 server.py". Then, navigate to localhost:3000 in a web browser to see the sample experiment. 

Note: If you want to add Maze functionality to an existing Ibex implementation (for instance, to run experiments on Ibex farm), these are the changed files:
* Addition of Maze.css and MazeSeparator.css in the css_includes folder
* Addition of Maze.js and MazeSeparator.js in the js_includes folder
* To test, replace contents of data_includes with sample.js 

## Options

If you're building maze materials automatically using <https://github.com/vboyce/Maze/tree/master/maze_automate>, you can get those materials in ibex-format, and just copy those lines into the items list of a ibex experiment file. 

If you're not, these are the available arguments and specifications. 

### Options for Maze: 
* s: Required. The correct sentence, either as a string or an array of words/chunks (same format as for spr). Usually starts with "The"
* a: Required. The alternative (distractor) options. Can be either a string or an array of words/chunks, needs to have the same number of words/chunks as s. Usually starts with "x-x-x". 
* order: An array of 0's and 1's, the same length as s. Indicates whether the correct answer should be the left (0) or right (1) of the two options. If unspecified, will be 0 followed by a pseudorandom order of 0s and 1s (this constrains the first pair to be "The x-x-x" followed by random). Note: the default options means that different participants will see different orders. If you want them to all see the same order, you should specify. 
* redo: Default is false. If redo is true, then the sentences do not terminate on errors, but instead show an error message ("Incorrect. Please try again.") until the correct key is selected. This mode may be useful to researchers who want to check materials (and therefore want to see the whole sentence, regardless of mistakes). It can be toggled on for an entire set of items by adding

> var defaults = ["Maze", {redo: true}];

to the top of the data file. (Note that to check *all* experimental items, you may need to relabel the types of sentences to override Latin square behavior.)
This mode can also be used when running the experiment; both the time until first press, and the total time to correct are recorded, so it you can tell how long participants are spending after making mistakes. (From some limited testing, this mode seems to work, and is useful if your items are long or you don't proofread your distractors.) We recommend you consider whether your experiment would benefit from having participants continue after mistakes or not. 
* time: An integer 0 or greater. Only relevant if redo:true, this is how many milliseconds to wait after an incorrect selection before registering the next selection. By default time=1000 (for a 1 second delay). To use redo with no delay, set time: 0. 
* emess: A string. Only relevant if redo:true and time>0. This is the message displayed after a mistake while presses are not registered. By default, the message is "Incorrect!"
* rmess: A string. Only relevant if redo:true. This is the message displayed after a mistake once time has elapsed and button presses will work. By default, the message is "Please try again.". If time:0, we only rmess will be seen, so we recommend changing it to something like "Incorrect! Please try again.". 

### Passing results to next item:
When a participant makes an incorrect selection, maze will record the time it took them to do so, but then it will stop that sentence, and pass "failed" to the next element. It is recommended to use "followEachWith" for maze items to follow each with a separator saying whether it was correct or not, so participants know when a new sentence is starting. 

Maze also displays a count of words gotten right so far. If you use the normal separator, the count will reset to 0 at the beginning of each item. If you want the count to be cumulative, you need to use MazeSeparator (.css and .js files included) to separate. All items that intervene between Maze tasks must contain the lines below for cumulative counting to work. 
> var x = this.utils.getValueFromPreviousElement("counter");

> if (x) this.utils.setValueForNextElement("counter",x);

Note that this means that if you have blocks, with a message in between blocks, the count will reset at the start of each block, which may be desirable.

## Result columns: 
The first seven are same as for other Ibex modules; see Ibex documentation for an explanation. 
* 8.Word number: Starting at 0 for the first (no-real-choice) word.
* 9.Word: The text of the correct word.
* 10.Alternative: The text of the distractor.
* 11.Word on (0=left, 1=right): Either 0 or 1 to indicate which side of the screen the correct word was displayed on. 
* 12.Correct: "yes" or "no" depending on whether the participant answered correctly. Note that "no" will be shown for words the participant did not see (i.e. words after the one they got wrong). In "redo" mode, this refers to the first button they press.
* 13.Reading time to first answer: in ms. Reading time is provided for all words a participant saw, but the 0-word reading time is assessed differently (and so may not be comparable with other words in the sentence). Reading times are given for the word a participant gets wrong. "None" is used for words a participant did not see. In "redo" mode, this is time to first press (either right or wrong).
* 14.Sentence. Text of the entire correct sentence. 
* 15.Total time to correct answer. If not "redo" mode, will duplicate column 13. In "redo" mode, this count the time from the start of the item to the correct answer which will be longer for incorrect answers. Subtract col 13 from this to get time spent correcting the error. Note that in "redo" mode with a delay (time>0), this will include time to first click, time spent on the delay, and time to correct click once allowed. 

