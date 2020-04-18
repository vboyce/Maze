import logging
import csv
from sentence_set import Sentence, Sentence_Set


def read_input(filename):
    '''Reads an input file
    Arguments:
    filename = a semicolon delimited file with the following information
    first column = any info that should stay associated with the sentence such as condition etc
    this will be copied to eventual output unchanged (but will be the condition info if ibex output format is used
    second column = item number.
    Third column = sentence
    Fourth column = labels; if it exists, must be same number of wo./d  rds as sentence. if it doesn't exist,
    will be given 1:n labels ()
    Returns:
    item_to_info = a dictionary of item numbers as keys and a pair of lists (conditions, sentences) as value
    sentences =  a list of sentences grouped by item number (ie will get matching distractors)'''
    all_sentences = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=";", quotechar='"')
        for row in reader:
            tag = row[0]
            id = row[1]
            word_sentence = row[2]
            words = word_sentence.split()
            if len(row) > 3:
                label_sentence = row[3]
                labels = label_sentence.split()
                if len(labels) != len(words):
                    if len(labels) == 0:
                        labels = list(range(0, len(words)))
                    else:
                        logging.error("Labels are wrong length for sentence %s", word_sentence)
                        raise ValueError
            else:
                labels = list(range(0, len(words)))
            if id not in all_sentences.keys():
                all_sentences[id] = Sentence_Set(id)
            all_sentences[id].add(Sentence(words, labels, id, tag))
    return all_sentences
