import numpy
import csv
import sys
import argparse
from random import shuffle

def scramble(sentence):
    while not sentence[-1].isalpha():
        sentence=sentence[:-1]
    split = sentence.split()  # Split the string into a list of words
    first = split[0]
    rest = split[1:]
    shuffle(rest)  # This shuffles the list in-place.
    return first+' '+' '.join(rest)  # Turn the list back into a string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Take materials and output an ibex maze data file')
    parser.add_argument('filename', metavar='Input', type=str, help='file with input in tsv format,'+
                        'first column sentences, second column item labels')
    parser.add_argument('write_to', metavar='Output', type=str, help='file to write output to')
    args=vars(parser.parse_args())
    with(open(args['filename'],"r")) as f:
        with(open(args['write_to'], "a")) as g:
            for i in f.readlines():
                g.write(scramble(i)+"\n")
