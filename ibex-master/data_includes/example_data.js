var shuffleSequence = seq("intro",followEachWith("sep","test"), "done");

var showProgressBar =false;

var items = [


    ["intro", "Message", {html: "This is a demo of the maze task implemented in ibex. You will read a sentence word by word. On each screen you will see two words, one of which is a reasonable continuation of the sentence. Use your left and right arrow buttons to indicate which word is the correct continuation. The sentence will start with 'the'." }],
    ["test", "Maze", {s: "The day was sunny.", a: "--- went warm and", order: [0,1,1,0]}],
    ["test", "Maze", {s: "The day was cloudy.", a: "--- blew wind because"} ],
    ["sep", "Separator", {normalMessage: "Correct! Press any key to continue", errorMessage: "Incorrect! Press any key to continue."}],
    ["done", "Message", {html: "All done!"}]
];
