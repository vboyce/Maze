import torch
from nltk.tokenize import word_tokenize
from gulordava_code import dictionary_corpus
from helper_new import specify, get_alt_nums, get_alts, strip_punct #combining helper helper_wf
from flexmatch import match
#### gulordava specific ####
which_freq = ""
def load_model(freq):
    '''sets up a model for gulordava
    Arguments: none
    Returns the model and device'''
    which_freq = freq
    specify(freq)
    with open("gulordava_data/hidden650_batch128_dropout0.2_lr20.0.pt", 'rb') as f:
        print("Loading the model")
        # to convert model trained on cuda to cpu model
        model = torch.load(f, map_location=lambda storage, loc: storage)
    model.eval() #put model in eval mode
    model.cpu() # put it on cpu
    device = torch.device("cpu") #what sort of data model is stored on
    return (model, device)

def load_dict():
    '''loads the dictionary
    Arguments: none
    Returns dictionary and length of dictionary'''
    dictionary = dictionary_corpus.Dictionary("gulordava_data") #load a dictionary
    ntokens = dictionary.__len__() #length of dictionary
    return (dictionary, ntokens)

def new_sentence(model, device, ntokens):
    '''sets up a new sentence for gulordava model
    Arguments: model, device as from load_model, ntokens = length of dictionary
    returns a word placeholder and an initialized hidden layer'''
    hidden = model.init_hidden(1) #sets initial values on hidden layer
    input_word = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device) #make a word placeholder
    return (input_word, hidden)

def update_sentence(word, input_word, model, hidden, dictionary):
    '''takes in a sentence so far adds the next word and returns the new list of surprisals
    Arguments:
    word = next word in sentence
    input_word = placeholder for wordid
    model = model from load_model
    hidden = hidden layer representation of sentence so far
    dictionary = dictionary from load_dict
    Returns: output = (probably not needed??)
    hidden = new hidden layer
    word_surprisals = distribution of surprisals for all words'''
    word = strip_punct(word)[0]
    parts = word_tokenize(word) #get list of tokens
    for part in parts:
        token = dictionary_corpus.tokenize_str(dictionary, part)[0] #get id of token
        # if part not in dictionary.word2idx:
        #    print("Good word "+part+" is unknown") #error message
        input_word.fill_(token.item()) #fill with value of token
        output, hidden = model(input_word, hidden) #do the model thing
        word_weights = output.squeeze().div(1.0).exp().cpu() #process output into weights
        word_surprisals = -1*torch.log2(word_weights/sum(word_weights))# turn into surprisals
    return (hidden, word_surprisals)

def get_surprisal(surprisals, dictionary, word, good_bad):
    '''Find the surprisal for a word given a context
    Arguments:
    surprisals - surprisal distribution
    dictionary - word to word id dictionary
    word - word we want surprisal for 
    Returns the numeric surprisal value of the word, if word is unknown returns -1
    We don't trust surprisal values for UNK words'''
    (word, _, _, _) = strip_punct(word)
    token = dictionary_corpus.tokenize_str(dictionary, word)[0] #take first token of word
    if word not in dictionary.word2idx:
        #if good_bad == 0:
        #    print("Good word " + word + " is unknown")
        #else:
        #    print("Bad word " + word + " is unknown")
        return -1 #use -1 as an error code
    if good_bad == 0:
        print(word, surprisals[token].item())
    return surprisals[token].item() #numeric value of word's surprisal

def find_bad_enough(num_to_test, min_abs, min_rel, word_list, surprisals_list, dictionary, used):
    '''Finds an adequate distractor word
    either the first word that meets minimum surprisal for all sentences or the best if
    it tries num_to_test and none meet the minimum
    Arguments:
    num_to_test = an integer for how many candidate words to try
    minimum = minimum surprisal desired
    (will return first word with at least this surprisal for all sentences)
    word_list = the good words that occur in this position
    surprisals_list = distribution of surprisals (from update_sentence)
    dictionary = word to word_id look up
    returns: chosen distractor word'''
    # find average surprisal for the good words
    base_surprisal = 0
    cnt = 0
    for j in range(len(surprisals_list)):
        surprisal = get_surprisal(surprisals_list[j], dictionary, word_list[j], 0) #get good word surprisal
        if (surprisal != -1):
            # ignore those which are unknown
            base_surprisal += surprisal
            cnt += 1
    if cnt == 0 or min_rel == -1:  # good words are all unknown or relative minimum is not specified, using the absolute minimum
        minimum = min_abs
        # print("Minimum threshold = "+str(minimum))
    else:  # use the higher minimum between the absolute and the relative
        base_surprisal /= cnt
        minimum = max(min_abs, base_surprisal + min_rel)
        # print("Minimum threshold = "+str(minimum))
    
    best_word = ""
    best_surprisal = 0
    (length, freq) = get_alt_nums(word_list)  # get average length, frequency
    options_list = get_alts(length, freq)
    i = 1
    k = 0
    while k < num_to_test:
        while k == len(options_list):  # if we run out of options
            options_list.extend(get_alts(length, freq + i))  # find words with that length and frequency
            options_list.extend(get_alts(length, freq - i))
            i += 1  # if there weren't any, try a slightly higher frequency
            if i > 100:  # dummy value higher than we expect any frequency to be
                break  # out of infinite loop
        word = options_list[k]
        k += 1
        if word in used:  # word has been used before in the sentence
            continue
        min_surprisal = 100  # dummy value higher than we expect any surprisal to actually be
        for j in range(len(surprisals_list)): # for each sentence
            surprisal = get_surprisal(surprisals_list[j], dictionary, word, 1)  # find that word
            min_surprisal = min(min_surprisal, surprisal)  # lowest surprisal so far
        if min_surprisal >= minimum:  # if surprisal in each condition is adequate
            return word # we found a word to use and are done here
        if min_surprisal > best_surprisal:  # if it's the best option so far, record that
            best_word = word
            best_surprisal = min_surprisal
        if i > 100:
            break  # out of infinite loop
    # print("Couldn't meet surprisal target, returning with surprisal of "+str(best_surprisal))  # return best we have
    return best_word


def do_sentence_set(sentence_set, matching_set, model, device, dictionary, ntokens, num_to_test, min_abs, min_rel, duplicate_words, match_type):
    '''Processes a set of sentences that get the same distractors
    Arguments:
    sentence_set = a list of sentences (all equal length)
    model, device = from load_model
    dictionary, ntokens = from load_dictionary
    returns a sentence format string of the distractors'''
    bad_words = []
    words = []
    # sentence_length = len(sentence_set[0].split()) #find length of first item
    # set up a "used words" set
    used = set()
    #if duplicate_words:
    #    print("Allowing duplicate words in a sentence")
    '''
    for i in range(len(sentence_set)):
        bad_words.append(["x-x-x"])
        sent_words = sentence_set[i].split()
        if len(sent_words) != sentence_length:
            print("inconsistent lengths!!")  #complain if they aren't the same length
        words.append(sent_words) # make a new list with the sentences as word lists
    '''
    print(sentence_set)
    id_to_pos = {}
    pos_to_word = {}
    pos_to_surprisals = {}
    id_to_badword = {}
    words_in_sentence = []
    keys_in_sentence = []
    sentence_length = -1
    # for auto matching, generate matching
    if match_type == 'auto':
        matching_set = match(sentence_set, 1)  # threshold: 1 for identical words only, less for similar words to be treated as identical words
    # for index matching, check of the sentence lengths are the same
    # preprocessing the input
    for i in range(len(sentence_set)):
        bad_words.append([])
        words_in_sentence.append(sentence_set[i].split())
        if match_type == 'index':
            if sentence_length == -1:
                # first sentence
                sentence_length = len(words_in_sentence[i])
            elif len(words_in_sentence[i]) != sentence_length:
                # not the first sentence, the length does not match with the first sentence
                raise ValueError("Matching failed: in this case the lengths of sentences must be the same")
        sentence_length = max(sentence_length, len(words_in_sentence[i]))
        keys_in_sentence.append(matching_set[i])
        if len(words_in_sentence[i]) != len(keys_in_sentence[i]):
            print(words_in_sentence[i])
            print(keys_in_sentence[i])
            raise ValueError("Matching failed: the sentence and the word IDs don't match in length")
        for j in range(len(words_in_sentence[i])):
            if keys_in_sentence[i][j] not in id_to_pos:
                id_to_pos[keys_in_sentence[i][j]] = [(i, j)]
            else:
                id_to_pos[keys_in_sentence[i][j]].append((i, j))
            pos_to_word[(i, j)] = words_in_sentence[i][j]
    # check to make sure that first words are only matched with first words
    for (id, pos_list) in id_to_pos.items():
        has_first = False
        has_nonfirst = False
        for pos in pos_list:
            if pos[1] == 0:
                has_first = True
            else:
                has_nonfirst = True
        if has_first and has_nonfirst:
            raise ValueError("Matching failed: the first words in some of the sentences are matched with other words that are not first in sentence")

    hidden = [None]*len(sentence_set)  # set up a bunch of stuff
    input_word = [None]*len(sentence_set)
    surprisals = [None]*len(sentence_set)
    for i in range(len(sentence_set)):  # more set up
        input_word[i], hidden[i] = new_sentence(model, device, ntokens)
    for j in range(sentence_length - 1):  # for each word position in the sentence
        for i in range(len(sentence_set)):  # for each sentence
            if j >= len(words_in_sentence[i]) - 1:  # if the sentence doesn't have as many words in the sentnece, skip
                continue
            hidden[i], surprisals[i] = update_sentence(words_in_sentence[i][j+1], input_word[i], model, hidden[i], dictionary)  # and the next word to the sentence
            pos_to_surprisals[(i, j + 1)] = surprisals[i]

    for id in id_to_pos:
        pos_list = id_to_pos[id]
        has_first = False
        for pos in pos_list:
            if pos[1] == 0:
                has_first = True
                break
        if has_first:
            # no need to find bad word, first word of the sentence
            continue
        word_list = [pos_to_word[pos] for pos in pos_list]
        surprisals = [pos_to_surprisals[pos] for pos in pos_list]
        bad_word = find_bad_enough(num_to_test, min_abs, min_rel, word_list, surprisals, dictionary, used)  # find an alternate word
        id_to_badword[id] = bad_word
        # add bad word to the set of used words
        if duplicate_words == False:
            used.add(bad_word)
        # using the surprisals and matching frequency for the good words

    bad_sentences = []
    # constructing bad sentences from the stored bad words and ordering of original words
    for i in range(len(sentence_set)):
        bad_split_sentence = ["x-x-x"]
        for j in range(1, len(words_in_sentence[i])):
            id = keys_in_sentence[i][j]
            word = id_to_badword[id]
            (_, prefix, suffix, case) = strip_punct(words_in_sentence[i][j])  # formatting
            if case == 2:  # all capitalized
                mod_bad_word = word.upper()
            elif case == 1:  # first letter capitalized
                if len(word) == 0:
                    mod_bad_word = ""
                elif len(word) == 1:
                    mod_bad_word = word[0].upper()
                else:
                    mod_bad_word = word[0].upper() + word[1:]
            else:  # all lowercase, keep the same word case
                mod_bad_word = word
            mod_bad_word = prefix + mod_bad_word + suffix  # match end punctuation
            bad_split_sentence.append(mod_bad_word)  # add the fixed bad word to a running list for that sentence
        bad_sentences.append(" ".join(bad_split_sentence))
    return bad_sentences  # and return
