var shuffleSequence = seq("intro", followEachWith("sep","practice"),followEachWith("sep","test"), "done");

var showProgressBar =false;

var items = [

	["intro", "Message", {html: "For this experiment, please place your left index finger on the 'e' key and your right index finger on the 'i' key. You will read sentences word by word. On each screen you will see two options: one will be the next word in the sentence, and one will not. Select the word that continues the sentence by pressing 'e' (left-hand) for the word on the left or pressing 'i' (right-hand) for the word on the right." }],
	["sep", "MazeSeparator", {normalMessage: "Correct! Press any key to continue", errorMessage: "Incorrect! Press any key to continue."}],
	["done", "Message", {html: "All done!"}],
	["practice", "Maze", {s: "This is a practice sentence.", a: "--- yo j coptuses cecorted."}],
	["practice", "Maze", {s: "Here is another practice sentence.", a: "--- ez debroms bentring knatchly."}],
	["practice", "Maze", {s: "Here is a sesquipedalian word", a:"--- blah blah blabbity blah"}],
	["practice", "Maze", {s: "After this sentence, the experiment will begin.", a: "--- weap roardage, pak sirelished jims zetus."}],
	["test", "Maze", {s: "The dog went to the park.", a: "--- odg netw ot teh arkp."}],
	["test", "Maze", {s: "The boy took the puppy to the park to play on the swings.", a: "--- byo toko eht upypp ot eht rpak ot alpy ln eth wigssn."}],
	["test", "Maze", {s: "The dog did not appreciate this.", a: "--- gdo idd otn tpracpeaei thsi."}],
	["test", "Maze", {s: "Look, a rainbow!", a: "--- u wbarnoi!"}]
];
