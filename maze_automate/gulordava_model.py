import torch
from nltk.tokenize import word_tokenize
from gulordava_code import dictionary_corpus
from helper_new import specify, get_alt_nums, get_alts, strip_end_punct #combining helper helper_wf
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
    return(dictionary, ntokens)

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
    parts = word_tokenize(word) #get list of tokens
    for part in parts:
        token = dictionary_corpus.tokenize_str(dictionary, part)[0] #get id of token
        if part not in dictionary.word2idx:
            print("Good word "+part+" is unknown") #error message
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
    token = dictionary_corpus.tokenize_str(dictionary, word)[0] #take first token of word
    if word not in dictionary.word2idx:
        if good_bad == 0:
            print("Good word " + word + " is unknown")
        else:
            print("Bad word " + word + " is unknown")
        return -1 #use -1 as an error code
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
    #find average surprisal for the good words
    base_surprisal = 0
    cnt = 0
    for j in range(len(surprisals_list)):
        surprisal = get_surprisal(surprisals_list[j], dictionary, strip_end_punct(word_list[j])[0], 0) #get good word surprisal
        if (surprisal != -1):
            #ignore those which are unknown
            base_surprisal += surprisal
            cnt += 1
    if (cnt == 0 or min_rel == -1): #good words are all unknown or relative minimum is not specified, using the absolute minimum
        minimum = min_abs
        print("Minimum threshold = "+str(minimum))
    else: #use the higher minimum between the absolute and the relative
        base_surprisal /= cnt
        minimum = max(min_abs, base_surprisal + min_rel)
        print("Minimum threshold = "+str(minimum))
    
    best_word = ""
    best_surprisal = 0
    (length, freq) = get_alt_nums(word_list) #get average length, frequency
    options_list = get_alts(length, freq)
    i = 1
    k = 0
    while k < num_to_test:
        while k == len(options_list): # if we run out of options
            options_list.extend(get_alts(length, freq + i))# find words with that length and frequency
            options_list.extend(get_alts(length, freq - i))
            i += 1 #if there weren't any, try a slightly higher frequency
            if (i > 100): #dummy value higher than we expect any frequency to be
                break #out of infinite loop
        word = options_list[k]
        k += 1
        if (word in used): #word has been used before in the sentence
            continue
        min_surprisal = 100 #dummy value higher than we expect any surprisal to actually be
        for j in range(len(surprisals_list)): # for each sentence
            surprisal = get_surprisal(surprisals_list[j], dictionary, word, 1) #find that word
            min_surprisal = min(min_surprisal, surprisal) #lowest surprisal so far
        if min_surprisal >= minimum: #if surprisal in each condition is adequate
            return word # we found a word to use and are done here
        if min_surprisal > best_surprisal: #if it's the best option so far, record that
            best_word = word
            best_surprisal = min_surprisal
        if (i > 100):
            break #out of infinite loop
    print("Couldn't meet surprisal target, returning with surprisal of "+str(best_surprisal)) #return best we have
    return best_word

def do_sentence_set(sentence_set, matching_set, model, device, dictionary, ntokens, num_to_test, min_abs, min_rel, duplicate_words):
    '''Processes a set of sentences that get the same distractors
    Arguments:
    sentence_set = a list of sentences (all equal length)
    model, device = from load_model
    dictionary, ntokens = from load_dictionary
    returns a sentence format string of the distractors'''
    bad_words = []
    words = []
    #sentence_length = len(sentence_set[0].split()) #find length of first item
    #set up a "used words" set
    used = set()
    if (duplicate_words == True):
        print("Allowing duplicate words in a sentence")
    '''
    for i in range(len(sentence_set)):
        bad_words.append(["x-x-x"])
        sent_words = sentence_set[i].split()
        if len(sent_words) != sentence_length:
            print("inconsistent lengths!!")  #complain if they aren't the same length
        words.append(sent_words) # make a new list with the sentences as word lists
    '''
    word_to_id = {}
    words_in_sentence = []
    keys_in_sentence = []
    #TODO: for index matching, check of the sentence lengths are the same
    #convert the sentences to the traditional 'index to index' matching
    for i in range(len(sentence_set)):
        #bad_words.append(["x-x-x"])
        bad_words.append([])
        words_in_sentence.append(sentence_set[i].split())
        keys_in_sentence.append(matching_set[i])
        if (len(words_in_sentence[i]) != len(keys_in_sentence[i])):
            raise ValueError("Matching failed: the sentence and the word IDs don't match in length")
        for j in range(len(words_in_sentence[i])):
            if (keys_in_sentence[i][j] not in word_to_id):
                word_to_id[keys_in_sentence[i][j]] = [words_in_sentence[i][j]]
            else:
                word_to_id[keys_in_sentence[i][j]].append(words_in_sentence[i][j])
    #constructing a 2D array resembling the traditional words array
    words = [[] for i in range(len(sentence_set))]
    keys = [[] for i in range(len(sentence_set))]
    for (id, words_of_id) in word_to_id.items():
        for i in range(len(sentence_set)):
            words[i].append(words_of_id[i%len(words_of_id)]) #filling up to the original number of sentences
            keys[i].append(id) #keeping track of the word ids
    sentence_length = len(words[0])
    hidden = [None]*len(sentence_set) #set up a bunch of stuff
    input_word = [None]*len(sentence_set)
    surprisals = [None]*len(sentence_set)
    for i in range(len(sentence_set)): # more set up
        input_word[i], hidden[i] = new_sentence(model, device, ntokens)
    for j in range(-1, sentence_length-1): # for each word position in the sentence
        word_list = []
        for i in range(len(sentence_set)): # for each sentence
            if (j > -1):
                hidden[i], surprisals[i] = update_sentence(words[i][j], input_word[i], model, hidden[i], dictionary) # and the next word to the sentence
            else: #special case: first word in a sentence
                hidden[i], surprisals[i] = update_sentence(words[i][j+1], input_word[i], model, hidden[i], dictionary) # and the next word to the sentence
            word_list.append(words[i][j+1]) #add the word after that to a list of words
        bad_word = find_bad_enough(num_to_test, min_abs, min_rel, word_list, surprisals, dictionary, used) #find an alternate word
        #add bad word to the set of used words
        if (duplicate_words == False):
            used.add(bad_word)
        #using the surprisals and matching frequency for the good words
        for i in range(len(sentence_set)):
            cap=word_list[i][0].isupper() # what is capitization of good word in ith sentence
            if cap: #capitalize it
                mod_bad_word=bad_word[0].upper()+bad_word[1:]
            else: #keep lower case
                mod_bad_word=bad_word
            mod_bad_word = mod_bad_word+strip_end_punct(word_list[i])[1] #match end punctuation
            bad_words[i].append(mod_bad_word) # add the fixed bad word to a running list for that sentence
    bad_sentences = []
    bad_split_sentences = []
    #converting the bad_words 2D array back to the original sentences
    for i in range(len(sentence_set)):
        bad_split_sentences.append(["x-x-x"])
        for j in range(1, len(words_in_sentence[i])):
            id = keys_in_sentence[i][j]
            bad_split_sentences[i].append(bad_words[i][keys[i].index(id)]) #consider using a dict instead of .index()
        bad_sentences.append(" ".join(bad_split_sentences[i]))
    return bad_sentences # and return
