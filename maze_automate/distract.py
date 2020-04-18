#!/usr/bin/env python3

import argparse
from main import run_stuff

parser = argparse.ArgumentParser(description='Auto-generate Maze materials')

parser.add_argument('input', type=str,
                    help='input file')
parser.add_argument('output', type=str,
                    help='output file')
parser.add_argument('-p','--parameters', type=str, default=None,
                    help='parameters file')
parser.add_argument('--format', choices=["ibex", "delim"], default="delim",
                    help='output format, either delimited or for ibex maze')
args = parser.parse_args()


'''Takes input, generates distractors, writes to output file
Arguments:
infile = where input is
outfile = where to write output to
lang_model = either "gulordava" or "one_b" for which language model to use
out_format = either "basic" (for a semicolon delimited output) or "ibex" for ibex ready output
Returns: none'''
if args.parameters==None:
    run_stuff(args.input, args.output, outformat=args.format)
else:
    run_stuff(args.input, args.output, parameters=args.parameters, outformat=args.format)
