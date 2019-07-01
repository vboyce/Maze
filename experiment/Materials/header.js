//for G-maze
var shuffleSequence = seq("code", "setcounter", "welcome", "intro-gram", "intro-practice", followEachWith("sep", "practice"), "end-practice", followEachWith("sep",randomize(anyOf(startsWith("rel"),startsWith("and"), startsWith("adverb"), startsWith("filler")))),  "explanation","instructions2", anyOf("questionnaire"),"topic","debriefing");

//for L-maze
//var shuffleSequence = seq("code", "setcounter", "welcome", "intro-lex", "intro-practice", followEachWith("sep", "practice"), "end-practice", followEachWith("sep",randomize(anyOf(startsWith("rel"),startsWith("and"), startsWith("adverb"), startsWith("filler")))),  "explanation","instructions2", anyOf("questionnaire"),"topic","debriefing");

var showProgressBar =false;

var defaults = [
		"Question", {
				as: ["yes", "no"],
        presentAsScale: false,
        presentHorizontally: false,
    },
];

var code = Math.floor(Math.random()*100000000);
var sendingResultsMessage = "The results are now being transferred.  Please wait.";
var completionMessage = "Thank you for your participation.  The results were successfully transmitted.  Your participation code is: " + code.toString();
var completionErrorMessage = "The transmission of the results failed.  Please contact online_experiment@mit.edu and retry the transmission again by clicking the link.  Your participation code is: " + code.toString();

var items = [
    ["code", "DashedSentence", {s:code.toString(), mode:"speeded acceptability", wordTime:1}],
	["setcounter", "__SetCounter__", { }],
    ["welcome", "Message", {html:'<table width="100%"><tr><td valign="top" align="right">Department of Brain and Cognitive Sciences<br>Massachusetts Institute of Technology<br>77 Massachusetts Avenue<br>Cambridge, MA 02139-4307, USA</tr></table>\
<h2>Thank you very much for your participation!</h2><p>This HIT is part of a MIT scientific research project. Your decision to complete this HIT is voluntary. There is no way for us to identify you. The only information we will have, in addition to your responses, is the time at which you completed the survey. The results of the research may be presented at scientific meetings or published in scientific journals. Clicking on the link below indicates that you are at least 18 years of age and agree to complete this HIT voluntarily.'}],
    ["explanation", "Form", {html:'How was your experience doing this task? What did you think of its length?<br/><textarea name="explanation" rows="3" cols="50" autofocus="true"></textarea>'}],
		["instructions2", "Message", {html:'Now please answer a couple of questions about your background.  In accordance with the ethics guidelines of the Massachusetts Institute of Technology, this information will be stored in anonymous form and it will be impossible to link it to you.'}],
    ["questionnaire", "Form", {html:'How old are you? <input type="text" name="age" size="2" maxlength="2" autofocus="true"/>'}],
    ["questionnaire", "Question", {q:"Please select your gender.", as:["Male", "Female", "Other"]}],
		["questionnaire", "Form", {html:'Please select your home state: <select name="state"> <option value="other">[other]</option> <option value="AL">AL</option> <option value="AK">AK</option> <option value="AS">AS</option> <option value="AZ">AZ</option> <option value="AR">AR</option> <option value="CA">CA</option> <option value="CO">CO</option> <option value="CT">CT</option> <option value="DE">DE</option> <option value="DC">DC</option> <option value="FM">FM</option> <option value="FL">FL</option> <option value="GA">GA</option> <option value="GU">GU</option> <option value="HI">HI</option> <option value="ID">ID</option> <option value="IL">IL</option> <option value="IN">IN</option> <option value="IA">IA</option> <option value="KS">KS</option> <option value="KY">KY</option> <option value="LA">LA</option> <option value="ME">ME</option> <option value="MH">MH</option> <option value="MD">MD</option> <option value="MA">MA</option> <option value="MI">MI</option> <option value="MN">MN</option> <option value="MS">MS</option> <option value="MO">MO</option> <option value="MT">MT</option> <option value="NE">NE</option> <option value="NV">NV</option> <option value="NH">NH</option> <option value="NJ">NJ</option> <option value="NM">NM</option> <option value="NY">NY</option> <option value="NC">NC</option> <option value="ND">ND</option> <option value="MP">MP</option> <option value="OH">OH</option> <option value="OK">OK</option> <option value="OR">OR</option> <option value="PW">PW</option> <option value="PA">PA</option> <option value="PR">PR</option> <option value="RI">RI</option> <option value="SC">SC</option> <option value="SD">SD</option> <option value="TN">TN</option> <option value="TX">TX</option> <option value="UT">UT</option> <option value="VT">VT</option> <option value="VI">VI</option> <option value="VA">VA</option> <option value="WA">WA</option> <option value="WV">WV</option> <option value="WI">WI</option> <option value="WY">WY</option> </select>'}],
    ["questionnaire", "Question", {q:"Please select the highest level of education you have attained:", as:["Less than high school", "High school graduate", "Some college", "2-year college degree", "4-year college degree", "Professional degree", "Doctorate"]}],
    ["questionnaire", "Question", {q:"What is your political affiliation?", as:["Democrat", "Republican", "Independent", "Other", "None", "Rather not say"]}],
    ["questionnaire", "Question", {q:"Are you a citizen of the United States?"}],
    ["questionnaire", "Question", {q:"Are you a native speaker of English?"}],
    ["questionnaire", "Question", {q:"Do you currently reside in the United States?"}],
    ["topic", "Form", {html:'Very briefly, what do you think this study is about?<br/><textarea name="topic" rows="3" cols="50" autofocus="true"></textarea>'}],
    ["debriefing", "Message", {html:'<p>Thank you.  You will receive the participation code on the next page.</p>\n\n<p>Purpose of this study (feel free to skip): We’re generally interested in how the human brain processes language. The present study is testing out a new method for studying what types of sentence constructions are easier or harder to read. Your data will help us to answer these questions.</p>'}],
	["intro-lex", "Message", {html: "<p>For this experiment, please place your left index finger on the 'e' key and your right index finger on the 'i' key. </p><p>On each screen you will see two options: one will be a word and one will be on a non-word. Select the real word by pressing 'e' (left-hand) for the option on the left or pressing 'i' (right-hand) for the option on the right.</p><p>The words will make a sentence.</p>" }],
	["intro-gram", "Message", {html: "<p>For this experiment, please place your left index finger on the 'e' key and your right index finger on the 'i' key.</p><p> You will read sentences word by word. On each screen you will see two options: one will be the next word in the sentence, and one will not. Select the word that continues the sentence by pressing 'e' (left-hand) for the word on the left or pressing 'i' (right-hand) for the word on the right.</p><p>Select the best word as quickly as you can, but without making too many errors.</p>"}],
	["intro-practice", "Message", {html: "The following items are for practice." }],
	["end-practice", "Message", {html: "End of practice. The experiment will begin next."}],
	["sep", "MazeSeparator", {normalMessage: "Correct! Press any key to continue", errorMessage: "Incorrect! Press any key to continue."}],
	["done", "Message", {html: "All done!"}],
