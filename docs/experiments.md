---
layout: default
---

# Some advice on experiment design and length

I haven't done testing on how long people will do Maze tasks for before they get annoyed, so this is just advice.

The Maze task is slow; use 1 second/ word as a ballpark for how long it will take to complete. I've had success with experiments that take around 20-25 minutes for the median attentive participant; I'd be wary of doing longer. This works out to around 1200 words in the experiment or roughly 100 items. 

If possible, use a block design to give participants short breaks. In testing my own materials, I find it cognitively demanding, and so I think it's nice to periodically put in breaks that give a good place for participants to pause and tell them how much progress they've made. 

In Ibex, it's easy to do this by adding the following at the bottom of an experiment file. It counts up the Maze items; and every 12 maze sentences shows a message saying how many items are left. 

```
function modifyRunningOrder(ro) {

  var new_ro = [];
  item_count=0;
  for (var i in ro) {
    var item = ro[i];
    if (item[0].type.startsWith("rel")|| item[0].type.startsWith("and") || item[0].type.startsWith("adverb")||item[0].type.startsWith("filler")) {
        item_count++;
        new_ro.push(item);
        if (item_count%12===0 & item_count<95){
            if (item_count===84){
                text="End of block. Only 1 block left!";
                }
            else {
                text="End of block. "+(8-(Math.floor(item_count/12)))+" blocks left.";
            }ro[i].push(new DynamicElement("Message", {html: text}));
        }
      } else {
      new_ro.push(item);
      }
  }
  return new_ro;
}
```

Use practice items. This is not a natural task and it might take some getting used to. Give participants a chance to see how it works, see what happens when they make mistakes, and find a comfortable pace before they get to items you care about. You might want practice items that start out easier than your experimental items. 

# Analysing results

Ibex outputs results in a slightly weird csv format. Here's what I use to process my data into a rectangular data format in R. 

Note that many of the fields of output are encoded as URLs, so if you material had commas you might see "%2C". We use url_decode from the urltools package to remedy this. 

The "time" and "MD5" fields collectively uniquely identify subjects. 
```
library(tidyverse)
library(stringr)
library(urltools)
read_in_data <- function(filename){
data <- read_csv(filename, comment="#", 
    col_names=c("time", "MD5", "controller", "item", "elem","type", "group", 
                "col_8", "col_9", "col_10", "col_11", "col_12", "col_13", "col_14", "col_15"), 
    col_types=cols(time=col_integer(),
                    MD5=col_character(),
                    controller=col_character(),
                    item=col_integer(),
                    elem=col_integer(),
                    type=col_character(),
                    group=col_character(),
                    col_8=col_character(),
                    col_9=col_character(),
                    col_10=col_character(),
                    col_11=col_character(),
                    col_12=col_character(),
                    col_13=col_character(),
                    col_14=col_character(),
                    col_15=col_character()
                    )) %>% mutate_all(url_decode) #deal with %2C issue
                                                      
#split off non-maze, participant level stuff and process them
  other <- filter(data, type %in% c("questionnaire")) %>% 
    select(time, MD5, col_8, col_9) %>% 
    group_by(time, MD5) %>%
    pivot_wider(names_from=col_8, values_from=col_9) %>% 
    type_convert()
    
# if you have comprehension questions or other questions types, process them as well

maze<- filter(data, controller=="Maze") %>% 
    select(time, MD5, type,group, word_num=col_8, word=col_9, distractor=col_10,
        on_right=col_11, correct=col_12, rt=col_13, sentence=col_14, total_rt=col_15) %>% 
    type_convert(col_types=cols(
      time=col_integer(),
      MD5=col_character(),
      type=col_character(),
      group=col_character(),
      word_num=col_integer(),
      word=col_character(),
      distractor=col_character(),
      on_right=col_logical(),
      correct=col_character(),
      rt=col_integer(),
      sentence=col_character(),
      total_rt=col_integer()
    )) %>% 
    left_join(other, by=c("time", "MD5")) #rejoin any comprehension questions etc. 
    
  maze
}

maze_results <- read_in_data("results_file_location")%>% 
  mutate(subject=paste(MD5, time),
         subject=factor(subject, levels=unique(subject), 
                        labels=1:length(unique(subject)))) %>% 
  select(-MD5, -time) %>% 
  write_rds("rectangular_data.rds")

```
