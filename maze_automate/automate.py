#!/usr/bin/python3

import csv
import argparse

parser = argparse.ArgumentParser(description='Auto-generate Maze materials')

parser.add_argument('input', type=str,
                    help='input')
parser.add_argument('output', type=str,
                    help='output file')
parser.add_argument('--model', choices=["gulordava", "one_b"], default="gulordava",
                    help='which model to use (gulordava or one_b)')
parser.add_argument('--format', choices=["ibex", "basic"], default="basic",
                    help='output format, either basic (for csv) or maze')

args = parser.parse_args()



        
def save_output(outfile, item_to_info, end_result):
    '''Saves results to a file in semicolon delimited format
    basically same as the original input with another column for distractor sentence
    Arguments:
    outfile = location of a file to write to
    item_to_info = (from read_input) dictionary of item number to lists of conditions and sentences
    end_result = list of sentence formatted distractor words (ordered somehow)
    Returns: none
    will write a semicolon delimited file with
    column 1 = "tag"/condition copied over from item_to_info (from input file)
    column 2 = item number
    column 3 = good sentence
    column 4 = string of distractor words in order. '''
    with open(outfile, 'w') as f:
        for key in item_to_info:
            for i in range(len(item_to_info[key][1])):
                f.write('"'+item_to_info[key][0][i]+'";')
                f.write('"'+key+'";')
                f.write('"'+item_to_info[key][1][i]+'";')
                f.write('"'+end_result[item_to_info[key][1][i]]+'"\n')

def save_ibex_format(outfile, item_to_info, end_result):
    '''Saves results to a file in ibex format
    File contents can be copied into the items list of a maze_ibex file
    Arguments:
    outfile = location of a file to write to
    item_to_info = (from read_input) dictionary of item number to lists of conditions and sentences
    end_result = list of sentence formatted distractor words (ordered somehow)
    Returns: none'''
    with open(outfile, 'w') as f:
        for key in item_to_info:
            for i in range(len(item_to_info[key][1])):
                f.write('[["'+item_to_info[key][0][i]+'", ')
                f.write(key+'], "Maze", {s:')
                f.write('"'+item_to_info[key][1][i]+'", a:')
                f.write('"'+end_result[item_to_info[key][1][i]]+'"}], \n')

def read_input(filename):
    '''Reads an input file
    Arguments:
    filename = a semicolon delimited file with the following information
    first column = any info that should stay associated with the sentence such as condition etc
    this will be copied to eventual output unchanged (but will be the condition info if ibex output format is used
    second column = item number. Sentences that share item number will get same distractors,
    and *Must* have same number of word.
    Third column = sentence
    Returns:
    item_to_info = a dictionary of item numbers as keys and a pair of lists (conditions, sentences) as value
    sentences =  a list of sentences grouped by item number (ie will get matching distractors)'''
    item_to_info = {}
    with open(filename, 'r') as tsv:
        f = csv.reader(tsv, delimiter=";", quotechar='"')
        for row in f:
            if row[1] in item_to_info: #item num already seen
                item_to_info[row[1]][0].append(row[0]) #add condition to the list
                item_to_info[row[1]][1].append(row[2].strip()) #add sentence to the list
            else:
                item_to_info[row[1]] = [[row[0]], [row[2].strip()]] # new item num, add a new entry
    sentences = []
    for item in sorted(item_to_info):
        sentences.append(item_to_info[item][1]) #make a list of sentences, grouped by item number
    return (item_to_info, sentences)



def run_gulordava(sentences):
    '''wrapper for using the gulordava model
    Arguments:
    sentences = list of grouped sentences
    Returns:
    distractor sentences in same order/grouping'''
    import gulordava
    end_result = {}
    model, device = gulordava.load_model() #set up
    dictionary, ntokens = gulordava.load_dict()
    for i, _ in enumerate(sentences): #process all the sentences
        bad = gulordava.do_sentence_set(sentences[i], model, device, dictionary, ntokens)
        for j, _ in enumerate(sentences[i]): #record results
            end_result[sentences[i][j]] = bad
    return end_result

def run_one_b(sentences):
    '''wrapper for using the one_b model
    Arguments:
    sentences = list of grouped sentences
    Returns:
    distractor sentences in same order/grouping'''
    import one_b
    end_result = {}
    sess, t = one_b.load_model() #set up
    dictionary = one_b.load_dict()
    for i, _ in enumerate(sentences): #process all the sentences
        bad = one_b.do_sentence_set(sentences[i], sess, t, dictionary)
        for j, _ in enumerate(sentences[i]): #record results
            end_result[sentences[i][j]] = bad
    return end_result

'''Takes input, generates distractors, writes to output file
Arguments:
infile = where input is
outfile = where to write output to
lang_model = either "gulordava" or "one_b" for which language model to use
out_format = either "basic" (for a semicolon delimited output) or "ibex" for ibex ready output
Returns: none'''
item_to_info, sentences = read_input(args.input) # read input
if args.model == "gulordava": #for gulordava
    end_result = run_gulordava(sentences)
elif args.model == "one_b": #for one b model
    end_result = run_one_b(sentences)
if args.format == "ibex": #save output
    save_ibex_format(args.output, item_to_info, end_result)
elif args.format =="basic": # save output
    save_output(args.output, item_to_info, end_result)
