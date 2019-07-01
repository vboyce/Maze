library(tidyverse)
library(stringr)
library(urltools)
#function reads in data from a maze file plus demographic, other questions.
read_in_data <- function(filename){
  #reads data in generically because different format for different controllers
  data <- read_csv(filename, comment="#", col_names=c("time", "MD5", "controller", "item", "elem",
                                                      "type", "group", "col_8", "col_9", "col_10", "col_11", "col_12", "col_13", "col_14"), col_types=cols(
                                                        time=col_integer(),
                                                        MD5=col_character(),
                                                        controller=col_character(),
                                                        item=col_integer(),
                                                        elem=col_integer(),
                                                        type=col_character(),
                                                        group=col_integer(),
                                                        col_8=col_character(),
                                                        col_9=col_character(),
                                                        col_10=col_character(),
                                                        col_11=col_character(),
                                                        col_12=col_character(),
                                                        col_13=col_character(),
                                                        col_14=col_character()
                                                      )) %>% mutate_all(url_decode) #deal with %2C issue
  
  order_seen <- data %>% 
    select(time, MD5, group) %>% 
    filter(!is.na(group)) %>% 
    unique() %>% 
    group_by(time, MD5) %>% 
    mutate(trial_num = 1:n()) %>% 
    type_convert()
  
  #split off non-maze, participant level stuff and process them
  demographics <- filter(data, type=="questionnaire"| type=="judgement" | type=="explanation"|type=="topic") %>% 
    select(time, MD5, col_8, col_9) %>% 
    spread(key=col_8, value=col_9) %>% 
    rename(education=`Please select the highest level of education you have attained:`,
           participant_gender=`Please select your gender.`,
           political=`What is your political affiliation?`,
           citizen=`Are you a citizen of the United States?`,
           native=`Are you a native speaker of English?`,
           resident=`Do you currently reside in the United States?`) %>% 
    type_convert()
  
  #take the Maze task results, relabel and type appropriately
  maze<- filter(data, controller=="Maze") %>% 
    select(time, MD5, type, group, word_num=col_8, word=col_9, distractor=col_10, on_right=col_11, correct=col_12, rt=col_13, sentence=col_14) %>% 
    type_convert(col_types=cols(
      time=col_integer(),
      MD5=col_character(),
      type=col_character(),
      group=col_integer(),
      word_num=col_integer(),
      word=col_character(),
      distractor=col_character(),
      on_right=col_logical(),
      correct=col_character(),
      rt=col_integer(),
      sentence=col_character()
    )) %>% 
    left_join(demographics, by=c("time", "MD5")) %>%  #add the demographics on
    left_join(order_seen, by=c("time", "MD5", "group"))
  maze
}


#function reads in data from an spr plus demographic, other questions.
read_spr <- function(filename){
  #reads data in generically because different format for different controllers
  data <- read_csv(filename, comment="#", col_names=c("time", "MD5", "controller", "item", "elem",
                                                      "type", "group", "col_8", "col_9", "col_10", "col_11", "col_12", "col_13", "col_14"), col_types=cols(
                                                        time=col_integer(),
                                                        MD5=col_character(),
                                                        controller=col_character(),
                                                        item=col_integer(),
                                                        elem=col_integer(),
                                                        type=col_character(),
                                                        group=col_integer(),
                                                        col_8=col_character(),
                                                        col_9=col_character(),
                                                        col_10=col_character(),
                                                        col_11=col_character(),
                                                        col_12=col_character(),
                                                        col_13=col_character(),
                                                        col_14=col_character()
                                                      )) %>% mutate_all(url_decode) #deal with %2C issue
  
  order_seen <- data %>% 
    select(time, MD5, group) %>% 
    filter(!is.na(group)) %>% 
    unique() %>% 
    group_by(time, MD5) %>% 
    mutate(trial_num = 1:n()) %>% 
    type_convert()
  
  #split off non-maze, participant level stuff and process them
  demographics <- filter(data, type=="questionnaire"| type=="judgement" | type=="explanation"|type=="topic") %>% 
    select(time, MD5, col_8, col_9) %>% 
    spread(key=col_8, value=col_9) %>% 
    rename(education=`Please select the highest level of education you have attained:`,
           participant_gender=`Please select your gender.`,
           political=`What is your political affiliation?`,
           citizen=`Are you a citizen of the United States?`,
           native=`Are you a native speaker of English?`,
           resident=`Do you currently reside in the United States?`) %>% 
    type_convert()
  
  
  comp_questions <- filter(data, controller=="Question"&type!="questionnaire") %>% 
    select(time, MD5, group, question=col_8, answer=col_9, is_correct=col_10) %>% 
    type_convert(col_types=cols(
      time=col_integer(),
      MD5=col_character(),
      type=col_character(),
      group=col_integer(),
      question=col_character(),
      answer=col_character(),
      is_correct=col_logical()
    ))
  
  accuracy <- comp_questions %>% 
    group_by(time, MD5) %>% 
    summarize(accuracy=sum(is_correct)/n())
  
  #take the Maze task results, relabel and type appropriately
  spr<- filter(data, controller=="DashedSentence") %>% 
    select(time, MD5, type, group, word_num=col_8, word=col_9,  rt=col_10, sentence=col_12) %>% 
    type_convert(col_types=cols(
      time=col_integer(),
      MD5=col_character(),
      type=col_character(),
      group=col_integer(),
      word_num=col_integer(),
      word=col_character(),
      rt=col_integer(),
      sentence=col_character()
    )) %>%  left_join(demographics, by=c("time", "MD5")) %>%  #add the demographics on
    left_join(order_seen, by=c("time", "MD5", "group")) %>% 
    left_join(comp_questions, by=c("time", "MD5", "group")) %>% 
    left_join(accuracy, by=c("time","MD5"))

spr
}

#spr
spr <- read_spr("../Data/Raw/spr_raw") %>% 
  mutate(subject=paste(MD5, time),
         subject=factor(subject, levels=unique(subject), labels=1:length(unique(subject)))) %>% 
  select(-MD5, -time)

write_rds(spr, "../Data/Processed/spr.rds")

#g-maze
g_maze <- read_in_data("../Data/Raw/g_raw") %>% 
  mutate(subject=paste(MD5, time),
         subject=factor(subject, levels=unique(subject), labels=1:length(unique(subject)))) %>% 
  select(-MD5, -time)

write_rds(g_maze, "../Data/Processed/g_maze.rds")

# l_maze
l_maze <- read_in_data("../Data/Raw/l_raw") %>% 
  filter(MD5!="229cdd37bc817c64825d55998e4c65a9"|time!="1532544984") %>% #filter out one participant where there's G-maze data in the L-maze file???
  mutate(subject=paste(MD5, time),
         subject=factor(subject, levels=unique(subject), labels=1:length(unique(subject)))) %>% 
  select(-MD5, -time)

write_rds(l_maze, "../Data/Processed/l_maze.rds")

# gulordava
gulo_maze <- read_in_data("../Data/Raw/gulo_raw") %>% 
  mutate(subject=paste(MD5, time),
         subject=factor(subject, levels=unique(subject), labels=1:length(unique(subject)))) %>% 
  select(-MD5, -time)

write_rds(gulo_maze, "../Data/Processed/gulo_maze.rds")

# one_b

one_b_maze <- read_in_data("../Data/Raw/one_b_raw") %>% 
  mutate(subject=paste(MD5, time),
         subject=factor(subject, levels=unique(subject), labels=1:length(unique(subject)))) %>% 
  select(-MD5, -time)

write_rds(one_b_maze, "../Data/Processed/one_b_maze.rds")

