#!/usr/bin/env python3

import csv
import argparse

parser = argparse.ArgumentParser(description='Auto-generate Maze materials')

parser.add_argument('input', type=str,
                    help='input')
parser.add_argument('output', type=str,
                    help='output file')
parser.add_argument('--model', choices=["gulordava", "one_b"], default="gulordava",
                    help='which model to use (gulordava or one_b)')
parser.add_argument('--freq', choices=["ngrams", "wordfreq"], default="ngrams",
                    help='where to get frequency data from, either ngrams (our scraping of the google ngrams corpus) or the wordfreq module')
parser.add_argument('--format', choices=["ibex", "basic"], default="basic",
                    help='output format, either basic (for csv) or maze')
parser.add_argument('--num_to_test', type=int, default=100,
                    help='number of words to test in the process of finding bad words')
parser.add_argument('--min_abs', type=int, default=21,
                    help='absolute threshold of surprisal for a bad word, default to 21')
parser.add_argument('--min_rel', type=int, default=-1,
                    help='relative threshold of surprisal for a bad word to compare with the good word')
parser.add_argument('--duplicate_words', action="store_true", default=False,
                    help='allow duplicate words to be in the same output sentence')
parser.add_argument('--matching', choices=["index", "manual", "auto"], default="index",
                    help='between santences with the same item number, which word matching method to be used (index, manual or auto)')
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
                f.write('"'+end_result[item_to_info[key][1][i]]+'";')
                f.write('"'+" ".join([str(id) for id in item_to_info[key][2][i]])+'"\n')


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


def read_input(filename, match_type):
    '''Reads an input file
    Arguments:
    filename = a semicolon delimited file with the following information
    first column = any info that should stay associated with the sentence such as condition etc
    this will be copied to eventual output unchanged (but will be the condition info if ibex output format is used
    second column = item number. Sentences that share item number will get same distractors,
    and *Must* have same number of word.
    Third column = sentence
    Fourth column = word keys (ids given to each word to indicate that they would match to the same bad_word
    Returns:
    item_to_info = a dictionary of item numbers as keys and a pair of lists (conditions, sentences) as value
    sentences =  a list of sentences grouped by item number (ie will get matching distractors)'''
    item_to_info = {}
    with open(filename, 'r') as tsv:
        f = csv.reader(tsv, delimiter=";", quotechar='"')
        for row in f:
            if row[1] in item_to_info:  # item num already seen
                item_to_info[row[1]][0].append(row[0])  # add condition to the list
                item_to_info[row[1]][1].append(row[2].strip())  # add sentence to the list
                if match_type == 'index' or match_type == 'auto':  # auto has not been implemented
                    item_to_info[row[1]][2].append([i for i in range(len(row[2].strip().split()))])
                elif match_type == 'manual':
                    item_to_info[row[1]][2].append(row[3].strip().split())  # add word keys to the list
            else:
                item_to_info[row[1]] = [[row[0]], [row[2].strip()]]  # new item num, add a new entry
                if match_type == 'index' or match_type == 'auto':  # auto has not been implemented
                    item_to_info[row[1]].append([[i for i in range(len(row[2].strip().split()))]])
                elif match_type == 'manual':
                    item_to_info[row[1]].append([row[3].strip().split()])  # add word keys to the list
    sentences = []
    for item in sorted(item_to_info):
        sentences.append((item_to_info[item][1], item_to_info[item][2]))  # make a list of sentences and word keys, grouped by item number
    return (item_to_info, sentences)


def run(which_model, freq, sentences_keys, num_to_test, min_abs, min_rel, duplicate_words, match_type):
    '''wrapper for using either model with either wordfreq to use
    Arguments:
    model = the model specified
    freq = frequency model specified
    sentences = list of grouped sentences
    Returns:
    distractor sentences in same order/grouping'''
    end_result = {}
    if which_model == "gulordava":
        import gulordava_model  # will be created to accommodate both gulordava and gulordava_wf
        model, device = gulordava_model.load_model(freq)  # set up
        dictionary, ntokens = gulordava_model.load_dict()
    elif which_model == "one_b":
        import one_b_model  # will be created to accommodate both one_b and one_b_wf
        sess, t = one_b_model.load_model(freq)
        dictionary = one_b_model.load_dict()

    for i in range(len(sentences_keys)):  # process all the sentences
        (sentences, keys) = sentences_keys[i]  # divide the (sentences, keys) tuple into sentences and word keys
        if which_model == "gulordava":
            bad = gulordava_model.do_sentence_set(sentences, keys, model, device, dictionary, ntokens, num_to_test, min_abs, min_rel, duplicate_words, match_type)
        elif which_model == "one_b":
            #TODO: refector and incorporate word keys feature (word matching)
            bad = one_b_model.do_sentence_set(sentences, sess, t, dictionary)
        for j, _ in enumerate(sentences): #record results
            end_result[sentences[j]] = bad[j]
    return end_result


'''Takes input, generates distractors, writes to output file
Arguments:
infile = where input is
outfile = where to write output to
lang_model = either "gulordava" or "one_b" for which language model to use
out_format = either "basic" (for a semicolon delimited output) or "ibex" for ibex ready output
Returns: none'''
item_to_info, sentences = read_input(args.input, args.matching) # read input
print("Number of bad words to test = " + str(args.num_to_test))
end_result = run(args.model, args.freq, sentences, args.num_to_test, args.min_abs, args.min_rel, args.duplicate_words, args.matching)
if args.format == "ibex":  # save output
    save_ibex_format(args.output, item_to_info, end_result)
elif args.format == "basic":  # save output
    save_output(args.output, item_to_info, end_result)
