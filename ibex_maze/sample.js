//for G-maze
var shuffleSequence = seq("intro-gram", "intro-practice", followEachWith("sep", "practice"), "end-practice", followEachWith("sep",randomize(anyOf(startsWith("rel"),startsWith("and"), startsWith("adverb"), startsWith("filler")))),  "instructions2");

var showProgressBar =false;

var items = [
		["instructions2", "Message", {html:'End of sample Maze experiment.'}],
	["intro-gram", "Message", {html: "<p>For this experiment, please place your left index finger on the 'e' key and your right index finger on the 'i' key.</p><p> You will read sentences word by word. On each screen you will see two options: one will be the next word in the sentence, and one will not. Select the word that continues the sentence by pressing 'e' (left-hand) for the word on the left or pressing 'i' (right-hand) for the word on the right.</p><p>Select the best word as quickly as you can, but without making too many errors.</p>"}],
	["intro-practice", "Message", {html: "The following items are for practice." }],
	["end-practice", "Message", {html: "End of practice. The experiment will begin next."}],
	["sep", "MazeSeparator", {normalMessage: "Correct! Press any key to continue", errorMessage: "Incorrect! Press any key to continue."}],
	["done", "Message", {html: "All done!"}],
	[["adverb_high", 72], "Maze", {s:"Kim will display the photos she took next month, but she won't show all of them.", a:"x-x-x milk dealing sit compel eat thin poem older, us thy scale soft ran eat soon."}],
[["adverb_low", 72], "Maze", {s:"Kim will display the photos she took last month, but she won't show all of them.", a:"x-x-x milk dealing sit compel eat thin poem older, us thy scale soft ran eat soon."}],
[["adverb_high", 71], "Maze", {s:"Bob will complete the project he started next month, but Fred won't finish his.", a:"x-x-x mere quantity sat suppose joy officer soul funds, fat Kiss inner throne ran."}],
[["adverb_low", 71], "Maze", {s:"Bob will complete the project he started last month, but Fred won't finish his.", a:"x-x-x mere quantity sat suppose joy officer soul funds, fat Kiss inner throne ran."}],
[["and_no_comma", 48], "Maze", {s:"The witness identified the man and his wife ran away from the police station.", a:"x-x-x creates relatively sky my ice mid meet air sale seen won either develop."}],
[["and_comma", 48], "Maze", {s:"The witness identified the man, and his wife ran away from the police station.", a:"x-x-x creates relatively sky my ice mid meet air sale seen won either develop."}],
[["and_no_comma", 47], "Maze", {s:"Jenny talked to the reporter and the photographer took pictures of the scene.", a:"x-x-x deeper net ran dividing mid thy transitional laws increase our nor knows."}],
[["and_comma", 47], "Maze", {s:"Jenny talked to the reporter, and the photographer took pictures of the scene.", a:"x-x-x deeper net ran dividing mid thy transitional laws increase our nor knows."}],
[["relative_high", 24], "Maze", {s:"The niece of the butler who scolded herself for losing the key was very upset.", a:"x-x-x swarm ill joy accord thy starter variety lot pushed ad our sky tone tubes."}],
[["relative_low", 24], "Maze", {s:"The niece of the butler who scolded himself for losing the key was very upset.", a:"x-x-x swarm ill joy accord thy starter variety lot pushed ad our sky tone tubes."}],
[["relative_high", 23], "Maze", {s:"The aunt of the waiter who trained herself to cook wanted to own a restaurant.", a:"x-x-x unto joy per midway net essence pattern map wars report ago we map correspond."}],
[["relative_low", 23], "Maze", {s:"The aunt of the waiter who trained himself to cook wanted to own a restaurant.", a:"x-x-x unto joy per midway net essence pattern map wars report ago we map correspond."}],
[["filler", 134], "Maze", {s:"The children of the rich man were spoiled, but they were charming and handsome.", a:"x-x-x anything oil nor lies net safe manages, law mode soil mobility ran clusters."}],
[["filler", 133], "Maze", {s:"Yesterday the wife of the politician discussed health care with old people.", a:"x-x-x sin both bad off refinement evolution cities none thin am quoted."}],
[["filler", 132], "Maze", {s:"The boyfriend of the model was killed in an accident while skiing last week.", a:"x-x-x detectors joy won shall sin prices sin put petition exist cigars tell hear."}],
[["filler", 131], "Maze", {s:"The cute girl who was on the cover of the magazine became a famous doctor.", a:"x-x-x clot done net mid sum nor apply gas eat velocity growth try injury assume."}],
[["filler", 130], "Maze", {s:"The writer of the novels thought himself to be a genius, but he wasn't.", a:"x-x-x issued sea lie derive measure islands map tax try lights, thy tax divine."}],
[["practice", 108], "Maze", {s:"The semester will start next week, but the students and teachers are not ready.", a:"x-x-x chivalry anti wages body sold, sin sky entitled sky concrete oil him goods."}],
[["practice", 107], "Maze", {s:"The mother of the prisoner sent him packages that contained cookies and novels.", a:"x-x-x placed dry arm amounted rare nor rhythmic fund authority blossom me defect."}],
[["practice", 105], "Maze", {s:"The reporter had dinner yesterday with the baseball player who Kevin admired.", a:"x-x-x invested joy reduce organisms rise sum attained tended sin Troop flowing."}],
[["filler", 112], "Maze", {s:"Jane and John studied math and history yesterday, but they failed the exams.", a:"x-x-x boy Door trouble lien me nations customers, tax vote months thy decks."}],
[["practice", 104], "Maze", {s:"The therapist set up a meeting with the upset woman and her husband yesterday.", a:"x-x-x socialism ten sit sum absence wave ran keeps exist dry sum settled remainder."}],
];
