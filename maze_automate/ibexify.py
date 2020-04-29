import logging
import csv
def ibexify(infile, outfile):
    """Takes delim formatted output in infile and write ibex formatted output to outfile
    Useful if you failed to specify or otherwise need to convert to ibex format"""
    with open(infile, 'r') as f:
        reader = csv.reader(f, delimiter=";", quotechar='"')
        with open(outfile, 'w+') as out:
            for row in reader:
                out.write('[["' + row[0] + '", ')
                out.write(repr(row[1]) + '], "Maze", {s:"')
                out.write(row[2] + '", a:"')
                out.write(row[3] + '"}], \n')