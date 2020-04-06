import csv
import logging
import ast

def set_params(file):
    """Takes a colon delimited file specifying various parameters,
    returns dictionary format of those parameters"""
    params = {}
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=":", quotechar='"')
        for row in reader:
            if row != []:
                if row[0].startswith('#'):
                    pass
                else:
                    params[row[0]] = ast.literal_eval(row[1].strip())
    # Check required parameters
    if params.get('min_delta', None) is None:
        logging.error("Min delta must be provided")
        raise ValueError
    if params.get('min_abs', None) is None:
        logging.error("Min abs must be provided")
        raise ValueError
    if params.get('num_to_test', None) is None:
        logging.error("num to test must be provided")
        raise ValueError
    return params
