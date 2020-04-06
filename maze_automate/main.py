import logging
import importlib
from set_params import set_params
from input import read_input
from output import save_ibex, save_delim


def run_stuff(infile, outfile, parameters="params.txt", outformat="delim"):
    """Takes an input file, and an output file location
    Does the whole distractor thing (according to specified parameters)
    Writes in outformat"""
    if outformat not in ["delim","ibex"]:
        logging.error("outfile format not understood")
        raise ValueError
    params = set_params(parameters)
    sents = read_input(infile)
    dict_class = getattr(importlib.import_module(params["dictionary_loc"]), params["dictionary_class"])
    d = dict_class(params)
    model_class = getattr(importlib.import_module(params["model_loc"]), params["model_class"])
    m = model_class()
    threshold_func = getattr(importlib.import_module(params["threshold_loc"]), params["threshold_name"])
    for ss in sents.values():
        ss.do_model(m)
        ss.do_surprisals(m)
        ss.make_labels()
        ss.do_distractors(m, d, threshold_func, params)
        ss.clean_up()
    if outformat=="delim":
        save_delim(outfile, sents)
    else:
        save_ibex(outfile, sents)
