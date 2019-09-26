/* This software is licensed under a BSD license; see the LICENSE file for details. */

define_ibex_controller({
name: "Maze",

jqueryWidget: {
    _init: function() {
        this.cssPrefix = this.options._cssPrefix;
        this.utils = this.options._utils;
        this.finishedCallback = this.options._finishedCallback
        if (typeof(this.options.s) == "string") {
            // replace all linebreaks (and surrounding space) with 'space-return-space'
            var inputString = this.options.s.replace(/\s*[\r\n]\s*/g, " \r ");
            this.words = inputString.split(/[ \t]+/);
        } else {
            assert_is_arraylike(this.options.s, "Bad value for 's' option of Maze.");
            this.words = this.options.s;
        }
	    if (typeof(this.options.a) == "string") {
            // replace all linebreaks (and surrounding space) with 'space-return-space'
            var inputString = this.options.a.replace(/\s*[\r\n]\s*/g, " \r ");
            this.alts = inputString.split(/[ \t]+/);
        } else {
            assert_is_arraylike(this.options.a, "Bad value for 'a' option of Maze.");
            this.alts = this.options.a;
        }
	    assert(this.alts.length == this.words.length, "'a' and 's' must be the same length.");
        defaultOrder=[];
        defaultOrder[0]=0;
	    for (var i = 1; i < this.words.length; ++i){
            defaultOrder[i] = Math.round(Math.random());
        }
	    //If no left-right order is provided, construct one randomly. 
	    this.order=dget(this.options, "order", defaultOrder);
	    assert_is_arraylike(this.order, "Bad value for 'order' option of Maze.");
	    assert(this.order.length == this.words.length, "'order' and 's' must be the same length.");
	    for (i = 0; i < this.words.length; ++i){
            assert(defaultOrder[i]==1||defaultOrder[i]==0, "elements of 'order' must be 0 or 1.");
        }
        
        this.redo=dget(this.options, "redo", false);
        assert(typeof(this.redo)===typeof(true), "Bad value for 'redo', must be true or false.");
 
        this.currentWord = 0;

        this.stoppingPoint = this.words.length;
        this.counter=$("<div>").addClass(this.cssPrefix + 'counter');
        this.arrow=$("<div>").addClass(this.cssPrefix + 'arrow');
        this.larrow=$("<div>").addClass(this.cssPrefix + 'larrow');
        this.rarrow=$("<div>").addClass(this.cssPrefix + 'rarrow');
        this.wordSpan=$("<div>").addClass(this.cssPrefix + 'words');
        this.leftWord=$("<div>").addClass(this.cssPrefix + 'lword');
        this.rightWord=$("<div>").addClass(this.cssPrefix + 'rword');
        this.error=$("<div>").addClass(this.cssPrefix + 'error');
        this.mainDiv= $("<div>");
        this.element.append(this.mainDiv);


    	if (typeof(this.options.s) == "string")
		this.sentenceDesc = csv_url_encode(this.options.s);
    	else
		this.sentenceDesc = csv_url_encode(this.options.s.join(' '));
       
        this.resultsLines = [];
        this.mazeResults = [];
	    this.correct=[];
        for (i = 0; i < this.words.length; ++i){
            this.mazeResults[i] = new Array(2);
	        this.correct[i]= "no";
        }
        this.previousTime = new Date().getTime();

        this.leftWord.html((this.order[this.currentWord]===0) ?
            this.words[this.currentWord]:this.alts[this.currentWord]);
        this.rightWord.html((this.order[this.currentWord]===0) ?
            this.alts[this.currentWord]:this.words[this.currentWord]);
        this.larrow.html("e");
        this.rarrow.html("i");
        this.error.html("");
        var x = this.utils.getValueFromPreviousElement("counter");
        if (x) this.wordsSoFar=x;
        else this.wordsSoFar=0;
        this.counter.html("Words so far: "+this.wordsSoFar);
        this.mainDiv.css('text-align', 'center');
        this.arrow.append(this.larrow);
        this.arrow.append(this.rarrow);
        this.wordSpan.append(this.leftWord);
        this.wordSpan.append(this.rightWord);
        this.mainDiv.append(this.counter);
        this.mainDiv.append(this.wordSpan);
        this.mainDiv.append(this.arrow);
        this.mainDiv.append(this.error);
        
        var t = this;
        var repeat = false;
        this.safeBind($(document), 'keydown', function(event) {
            var time = new Date().getTime();
            var code = event.keyCode;

            if (code == 69 || code==73) {
                var word = t.currentWord;
                if (word <= t.stoppingPoint) {
		            t.correct[word]=((code==69 && t.order[word]==0)||
		                (code==73 && t.order[word]==1)) ? "yes" : "no";
	                if (!repeat){
		                var rs = t.mazeResults[word];
		                rs[0] = time;
                        rs[1] = t.previousTime;
                        }
		            if (t.correct[word]=="no" & t.redo){
		                t.error.html("Incorrect. Please try again.");
		                repeat = true;
		                return true;
		                }
		            else if (t.correct[word]=="no"){
		                t.utils.setValueForNextElement("failed", true);
		                t.utils.setValueForNextElement("counter", t.wordsSoFar);
		                t.processMazeResults();
		                t.finishedCallback(t.resultsLines);
		                return true;
		                }
	                if (t.correct[word] =="yes") {
	                    t.error.html("");
	                    repeat=false;
	                    }
		            
                }
                
                t.previousTime = time;
                ++(t.currentWord);
                if (t.currentWord >= t.stoppingPoint) {
                    t.utils.setValueForNextElement("counter", t.wordsSoFar);
                    t.processMazeResults();
                    t.finishedCallback(t.resultsLines);
                    return true;
                }
                t.showWord(t.currentWord);
                return false;
            }
            else {
                return true;
            }
        });
            
        },

    showWord: function (w) {
        if (this.currentWord < this.stoppingPoint) {
            this.leftWord.html((this.order[this.currentWord]===0) ?
                this.words[this.currentWord]:this.alts[this.currentWord]);
            this.rightWord.html((this.order[this.currentWord]===0) ?
                this.alts[this.currentWord]:this.words[this.currentWord]);
            this.wordsSoFar++;
            this.counter.html("Words so far: "+this.wordsSoFar);
        }
    },

    processMazeResults: function () {
        var nonSpaceWords = [];
        var nonSpaceAlts =[];
        for (var i = 0; i < this.words.length; ++i) {
	        nonSpaceWords.push(this.words[i]);
	        nonSpaceAlts.push(this.alts[i]);
        }

        for (var i = 0; i < nonSpaceWords.length; ++i) {
            this.resultsLines.push([
                ["Word number", i],
                ["Word", csv_url_encode(nonSpaceWords[i])],
                ["Alternative", csv_url_encode(nonSpaceAlts[i])],
                ["Word on (0=left, 1=right)", this.order[i]],
                ["Correct", this.correct[i]],
                ["Reading time", this.mazeResults[i][0] - this.mazeResults[i][1]],
                ["Sentence", this.sentenceDesc]
            ]);
        }
    }
},

properties: {
    obligatory: ["s", "a"],
    htmlDescription: function (opts) {
        return $(document.createElement("div")).text(opts.s);
    }
}
});
