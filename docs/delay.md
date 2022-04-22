---
layout: default
---

# Redo mode with delay: aligning incentives

Redo mode as first implemented was a big improvement, but it doesn't fully address one issue: aligning incentives. We as researchers would like participants to do the tasks as intended, so that their responses are useable data and mean what we think they mean. In the case of Maze, that means we'd like participants to choose the correct word as quickly as they can and try to read as "normally" as possible in this non-natural task.

Crowdworkers who are being paid per task are financially incentivized to do the task as fast as possible so as to maximize earnings. Obviously, crowdworkers vary in their motivations for doing tasks, and many care about doing the task well and contributing to science. However, it's better if there's less of a gap between how fast one could complete the task and how long it takes to do the task as intended; as then those who do the task as intended aren't losing out by being cooperative, and thus who just want to do it quickly for the money will be likely to do it as intended, and thus contribute usable data.

Maze without redo is horrible on this metric: The efficient thing to do is press i (or e), and it's very efficient and painless! You make mistakes quickly, and skip to the next sentence, and repeat. There are on average 2 clicks / sentence (+ 1 to go to the next sentence). 

Maze with redo (but no delay) is better, but still not great. You now have to randomly jam i and e (maybe alternating) a lot. It's annoying, because you now have to press on average 1.5 keys per word per sentence, but it's still faster than doing the task.

Maze with delay could bring incentives into closer alignment. Now each time you make a mistake you have to wait a delay period (like 1 second) before your keypresses register again. This should substantially slow down the random clicking method, and make it more annoying. It will also slightly slow down the doing-the-intended-task method (mistakes happen). I hope that with maze-with-delay following the sentence context will feel like the better option compared to button jamming. 

## But what time delay to use?

This is new and I don't have any empirical evidence. 1000ms (the default) is arbitrary, but it's roughly on par with how long it takes to make a selection when doing the task as intended. It also seems like enough time to register that it says "incorrect", but not long enough to be stuck pondering "why was that wrong?" (important given that sometimes errors reflect bad distractors rather than inattention or misclicking) or lose the sentence context. It may turn out that this is too long and than a shorter delay like 500ms makes more sense. 

To change the delay just change the line to specify the time delay you want.
```
var defaults = ["Maze", {redo: true, time:500}];
```
You can also change the messages people see, both directly after the mistake when they can't select and when they are free to try again.
```
var defaults = ["Maze", {redo: true, emess:"Oops! Please wait...", rmess:"Now try again.!"}];
```
## On the topic of incentives...
One common way to align financial incentives with research goals is to use performance bonuses. One could consider rewarding participants for having a high accuracy rate. It might need to be carefully tuned so that participants don't slow down too much (trying to be too careful) or get too upset at inevitable mistakes from bad distractors. 

I have not tried this, but it should be straightforward to calculate error rates for each participant. 
