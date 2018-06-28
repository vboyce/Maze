var shuffleSequence = seq("intro",followEachWith("sep","test"), "done");

var showProgressBar =false;

var items = [


	["intro", "Message", {html: "For this experiment, please place your left index finger on the 'e' key and your right index finger on the 'i' key. You will read sentences word by word. On each screen you will see two options: one will be the next word in the sentence, and one will not. Select the word that continues the sentence by pressing 'e' (left-hand) for the word on the left or pressing 'i' (right-hand) for the word on the right." }],
    ["test", "Maze", {s: "The day was sunny.", a: "--- went warm and", order: [0,1,1,0]}],
    ["test", "Maze", {s: "The day was cloudy.", a: "--- blew wind because"} ],
    ["test", "Maze", {s: "The doctor said that she had two months to live.", a: "--- he pretty and grow extreme fly give false blue",}],
    ["test", "Maze", {s: "The dog went to the park.", a: "--- hlh bodf ks dhd atuj."}],
    ["test", "Maze", {s: "Look, a rainbow!", a: "--- c acizavy!"}],
    ["sep", "MazeSeparator", {normalMessage: "Correct! Press any key to continue", errorMessage: "Incorrect! Press any key to continue."}],
    ["done", "Message", {html: "All done!"}]
];
