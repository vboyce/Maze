import csv

def save_delim(outfile, all_sentences):
    '''Saves results to a file in semicolon delimited format
    basically same as the original input with another column for distractor sentence
    Arguments:
    outfile = location of a file to write to
    all_sentences: dictionary of sentence_set objects
    Returns: none
    will write a semicolon delimited file with
    column 1 = "tag"/condition copied over from item_to_info (from input file)
    column 2 = item number
    column 3 = good sentence
    column 4 = string of distractor words in order.
    column 5 = string of labels in order. '''
    with open(outfile, 'w', newline="") as f:
        writer=csv.writer(f,delimiter=";")
        for sentence_set in all_sentences.values():
            for sentence in sentence_set.sentences:
                writer.writerow([sentence.tag,sentence.id,sentence.word_sentence,sentence.distractor_sentence,sentence.label_sentence])


def save_ibex(outfile, all_sentences):
    '''Saves results to a file in ibex format
    File contents can be copied into the items list of a maze_ibex file
    Arguments:
    outfile = location of a file to write to
    all_sentences: dictionary of sentence_set objects
    Returns: none'''
    with open(outfile, 'w') as f:
        for sentence_set in all_sentences.values():
            for sentence in sentence_set.sentences:
                f.write('[["'+sentence.tag+'", ')
                f.write(repr(sentence.id)+'], "Maze", {s:"')
                f.write(sentence.word_sentence+'", a:"')
                f.write(sentence.distractor_sentence+'"}], \n')
