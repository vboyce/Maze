library(tidyverse)
library(stringr)


read_raw_data <- function(data_source){
raw_data <- read_tsv(data_source, col_names=F) %>% 
  extract(X1, into=c("useless", "subject"), regex="(Subject) ([0-9]+)", remove=F) %>% 
  fill(subject) %>% 
  extract(X1, into=c("itemword", "error","rt"), regex="([0-9]+)\\s+(-?)([0-9.]+)", remove=F, convert=F) %>% 
  filter(is.na(useless)) %>% 
  filter(!is.na(itemword)) %>% 
  mutate(correct=ifelse(error=="-", "no", "yes"),
         item_num=as.integer(str_sub(itemword,1, -4)), #take the number part, but not the last 3 digits
         word_num=as.integer(str_sub(itemword,-3,)),  #end number part is word number
         rt=as.numeric(rt),
         subject=as.numeric(subject)) %>% 
  select(item_num, word_num, correct, rt, subject)
raw_data
}

read_materials <- function(filename){
text <- read_tsv(filename, col_names=F) %>% #read in line
  mutate(is_correct=str_sub(X1,1,1)) %>%  #pick out first character in line
  filter(is_correct %in% c("=","-","+")) %>%  #select only rows with answers, we ~don't care about the rest
  mutate(cleaner=str_replace_all(X1, '%75"READY"/ ', ""))%>% 
  separate(cleaner, c("a","b","c","d","e", "f", "g", "h"), sep=" ") %>% #separate on white space as a first pass
  separate(f, c("i","j"), sep='"') %>% #separate on quote mark
  mutate(item_num=as.integer(str_sub(a,2, -4)), #take the number part, but not the last 3 digits
         word_num=as.integer(str_sub(a,-3,)), #end number part is word number
         word_1=str_sub(c,3,), #select out the first word
         word_2=i) %>% #select the second word
  select(is_correct, item_num, word_num, word_1, word_2) #remove everything else 

by_correct <- text %>% #re-sort by correct/distractor rather than left/right
  mutate(word = ifelse(is_correct=="+", word_2, word_1),
         distractor = ifelse(is_correct=="+", word_1, word_2),
         target_placement = ifelse(is_correct=="+", 1, 0)) %>% 
  select(item_num, word_num, word, distractor, target_placement)

correct <- by_correct %>% #for each item_num, turn the correct items into a sentence
  select(item_num, word_num, word) %>% 
  spread(word_num, word, fill="") %>% 
  unite(sentence,-item_num, sep=" ") %>% #stick the words together into one column
  mutate(sentence=trimws(sentence)) %>% #cut off trailing whitespace due to differing word lengths
  select(item_num, sentence)

materials <- by_correct %>% left_join(correct, by="item_num")
}

#G-maze
#parse materials
w2012g1 <- read_materials("../Witzel/Witzel2012G1.txt") %>% 
  mutate(type=case_when(
    item_num < 13 ~ "relative_low", #relative clause with low attatchment
    item_num < 25 ~ "relative_high", #relative clause with high attatchment
    item_num < 37 ~ "and_comma", # NP/S conjunct with comma
    item_num < 49 ~ "and_no_comma", #NP/S conjunct ambiguity with no comma
    item_num < 61 ~ "adverb_low", #time adverbial with low attatchment
    item_num < 73 ~"adverb_high", #time adverbial with high attatchment
    item_num < 109 ~ "practice", #practice item
    TRUE ~ "filler" #else it's a filler. 
  ))

w2012g2 <- read_materials("../Witzel/Witzel2012G2.txt") %>% 
  mutate(type=case_when(
    item_num < 13 ~ "relative_high", #relative clause with high attatchment
    item_num < 25 ~ "relative_low", #relative clause with low attatchment
    item_num < 37 ~ "and_no_comma", # NP/S conjunct with no comma
    item_num < 49 ~ "and_comma", #NP/S conjunct with comma
    item_num < 61 ~ "adverb_high", #time adverbial with high attatchment
    item_num < 73 ~"adverb_low", #time adverbial with low attatchment
    item_num < 109 ~ "practice", #practice item
    TRUE ~ "filler" #else it's a filler. 
  ))

#parse data and join
g_data_1 <- read_raw_data("../Witzel/G_data_1.txt") %>% left_join(w2012g1, by=c("item_num", "word_num"))
g_data_2 <- read_raw_data("../Witzel/G_data_2.txt") %>% left_join(w2012g2, by=c("item_num", "word_num")) %>% 
  mutate(subject=subject+1000)
g_data_all <- g_data_1 %>% union(g_data_2) %>% mutate(subject=factor(subject, levels=unique(subject), labels=1:length(unique(subject))))%>% rename(group=item_num)

write_rds(g_data_all, "../Witzel/G_data.rds")

#L-maze
#parse materials
w2012l1 <- read_materials("../Witzel/Witzel2012L1.txt") %>% 
  mutate(type=case_when(
    item_num < 13 ~ "relative_low", #relative clause with low attatchment
    item_num < 25 ~ "relative_high", #relative clause with high attatchment
    item_num < 37 ~ "and_comma", # NP/S conjunct with comma
    item_num < 49 ~ "and_no_comma", #NP/S conjunct ambiguity with no comma
    item_num < 61 ~ "adverb_low", #time adverbial with low attatchment
    item_num < 73 ~"adverb_high", #time adverbial with high attatchment
    item_num < 109 ~ "practice", #practice item
    TRUE ~ "filler" #else it's a filler. 
  ))

w2012l2 <- read_materials("../Witzel/Witzel2012L2.txt") %>% 
  mutate(type=case_when(
    item_num < 13 ~ "relative_high", #relative clause with high attatchment
    item_num < 25 ~ "relative_low", #relative clause with low attatchment
    item_num < 37 ~ "and_no_comma", # NP/S conjunct with no comma
    item_num < 49 ~ "and_comma", #NP/S conjunct with comma
    item_num < 61 ~ "adverb_high", #time adverbial with high attatchment
    item_num < 73 ~"adverb_low", #time adverbial with low attatchment
    item_num < 109 ~ "practice", #practice item
    TRUE ~ "filler" #else it's a filler. 
  ))

#parse data and join
l_data_1 <- read_raw_data("../Witzel/L_data_1.txt") %>% left_join(w2012l1, by=c("item_num", "word_num"))
l_data_2 <- read_raw_data("../Witzel/L_data_2.txt") %>% left_join(w2012l2, by=c("item_num", "word_num")) %>% 
  mutate(subject=subject+1000)
l_data_all <- l_data_1 %>% union(l_data_2) %>% mutate(subject=factor(subject, levels=unique(subject), labels=1:length(unique(subject)))) %>% rename(group=item_num)

write_rds(l_data_all, "../Witzel/L_data.rds")

#SPR
read_SPR_data <- function(data_source){
  raw_data <- read_tsv(data_source, col_names=F) %>% 
    extract(X1, into=c("useless", "subject"), regex="(Subject) ([0-9]+)", remove=F) %>% 
    fill(subject) %>% 
    extract(X1, into=c("itemword", "error","rt"), regex="([0-9]+)\\s+(-?)([0-9.]+)", remove=F, convert=F) %>% 
    filter(is.na(useless)) %>% 
    filter(!is.na(itemword)) %>% 
    mutate(correct=ifelse(error=="-", "no", "yes"),
           item_num=as.integer(str_sub(itemword,1, -4)), #take the number part, but not the last 3 digits
           word_num=as.integer(str_sub(itemword,-3,)),  #end number part is word number
           rt=as.numeric(rt),
           subject=as.numeric(subject)) %>% 
    select(item_num, word_num, correct, rt, subject)
  
  comp_question <- raw_data %>% filter(word_num==251) %>% 
    mutate(is_correct=ifelse(correct=="yes", 1,0)) %>% 
    select(item_num, is_correct, subject)
  
  accuracy <- comp_question %>% 
    group_by(subject) %>% 
    summarize(accuracy=sum(is_correct)/n())
  
  cleaner_data <- raw_data %>% filter(word_num!=251) %>%  select(-correct) %>% left_join(comp_question, by=c("item_num","subject")) %>% 
    filter(word_num!=0) %>% mutate(word_num=word_num-1) %>% left_join(accuracy, by=c("subject"))

  cleaner_data
}
  
read_SPR_materials <- function(source){
text <- read_tsv(source, col_names=F) %>% #read in line
  mutate(is_correct=str_sub(X1,1,1),
         number=as.numeric(str_extract(X1, "[0-9]+")),
         item_num=ifelse(number<1000, number, number%/%1000),
         rest=str_sub(X1, 2,),
         rest=str_extract(rest, "[a-zA-Z,?.'\\-\\s\"]+"),
         item_part=ifelse(number<1000, NA, number%%1000)) %>%  #pick out first character in line
  filter(is_correct %in% c("=","-","+", "!"))  #select only rows with answers, we ~don't care about the rest

questions <- text %>% filter(item_part==251) %>% #prep questions
  separate("rest", into=c("a", "question", "c"), sep="[^a-zA-Z?'\\s]") %>% 
  mutate(cor_resp=ifelse(is_correct=="-", "no", "yes")) %>% 
  select(item_num, question, cor_resp)

sentences <- text %>% filter(is.na(item_part)) %>% #do sentences
  separate("rest", into=c("sentence"), sep="[;]") %>% 
  mutate(sentence=trimws(sentence)) %>% 
  select(item_num, sentence) %>% 
  left_join(questions) #add questions

words <- text %>% filter(is_correct=='+') %>% filter(!is.na(item_part)) %>% filter(item_part!=251) %>% filter(item_part!=0) %>% 
  extract(rest, into=c("word"), regex="([a-zA-Z]+[.,]?)", remove=F) %>% 
  mutate(word_num=item_part-1) %>% select(item_num, word_num, word) %>% left_join(sentences, by="item_num")

words}


w2012spr1 <- read_SPR_materials("../Witzel/Witzel2012SPR1.txt") %>% 
  mutate(type=case_when(
    item_num < 13 ~ "relative_low", #relative clause with low attatchment
    item_num < 25 ~ "relative_high", #relative clause with high attatchment
    item_num < 37 ~ "and_comma", # NP/S conjunct with comma
    item_num < 49 ~ "and_no_comma", #NP/S conjunct ambiguity with no comma
    item_num < 61 ~ "adverb_low", #time adverbial with low attatchment
    item_num < 73 ~"adverb_high", #time adverbial with high attatchment
    item_num < 109 ~ "practice", #practice item
    TRUE ~ "filler" #else it's a filler. 
  ))

w2012spr2 <- read_SPR_materials("../Witzel/Witzel2012SPR2.txt") %>% 
  mutate(type=case_when(
    item_num < 13 ~ "relative_high", #relative clause with high attatchment
    item_num < 25 ~ "relative_low", #relative clause with low attatchment
    item_num < 37 ~ "and_no_comma", # NP/S conjunct with no comma
    item_num < 49 ~ "and_comma", #NP/S conjunct with comma
    item_num < 61 ~ "adverb_high", #time adverbial with high attatchment
    item_num < 73 ~"adverb_low", #time adverbial with low attatchment
    item_num < 109 ~ "practice", #practice item
    TRUE ~ "filler" #else it's a filler. 
  ))

#parse data and join
spr_data_1 <- read_SPR_data("../Witzel/SPR_data_1.txt") %>% left_join(w2012spr1, by=c("item_num", "word_num"))
spr_data_2 <- read_SPR_data("../Witzel/SPR_data_2.txt") %>% left_join(w2012spr2, by=c("item_num", "word_num")) %>% 
  mutate(subject=subject+1000)
spr_data_all <- spr_data_1 %>% union(spr_data_2) %>% mutate(subject=factor(subject, levels=unique(subject), labels=1:length(unique(subject))))%>% rename(group=item_num)

write_rds(spr_data_all, "../Witzel/SPR_data.rds")
