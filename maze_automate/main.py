import logging
import importlib
from set_params import set_params
from input import read_input
from output import save_ibex, save_delim
import os.path

def run_stuff(infile, outfile, parameters="params.txt", outformat="delim"):
    """Takes an input file, and an output file location
    Does the whole distractor thing (according to specified parameters)
    Writes in outformat"""
    if outformat not in ["delim", "ibex"]:
        logging.error("outfile format not understood")
        raise ValueError
    params = set_params(parameters)
    sents = read_input(infile)
    dict_class = getattr(importlib.import_module(params.get("dictionary_loc", "wordfreq_distractor")),
                         params.get("dictionary_class", "wordfreq_English_dict"))
    d = dict_class(params)
    model_class = getattr(importlib.import_module(params.get("model_loc", "gulordava")),
                          params.get("model_class", "gulordava_model"))
    m = model_class()
    threshold_func = getattr(importlib.import_module(params.get("threshold_loc", "wordfreq_distractor")),
                             params.get("threshold_name", "get_thresholds"))
    for ss in sents.values():
        ss.do_model(m)
        ss.do_surprisals(m)
        ss.make_labels()
        ss.do_distractors(m, d, threshold_func, params)
        ss.clean_up()
    if outformat == "delim":
        save_delim(outfile, sents)
    else:
        save_ibex(outfile, sents)
