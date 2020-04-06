import wordfreq
import re
import math
import random
import logging

import utils
from distractor import distractor_dict, distractor


class wordfreq_English_dict(distractor_dict):
    """Dictionary built using word freq for frequencies
     Words need to be in wordfreq's vocab, also in include file if provided
     and not in exclude file
     words must be lowercase alpha only"""

    def __init__(self, params={}):
        exclude = params.get("exclude_words", "exclude.txt")
        include = params.get("include_words", "gulordava_data/vocab.txt")
        dict = wordfreq.get_frequency_dict('en')
        keys = dict.keys()
        self.words = []
        exclusions = []

        if exclude is not None:
            with open(exclude, "r") as f:
                for line in f:
                    word = line.strip()
                    exclusions.append(word)
        inclusions = []
        if include is not None:
            with open(include, "r") as f:
                for line in f:
                    word = line.strip()
                    inclusions.append(word)
            words = list(set(inclusions) & set(keys) - set(exclusions))
        else:
            words = list(set(keys) - set(exclusions))
        for word in words:
            if re.match("^[a-z]*$", word):
                freq = math.log(
                    dict[word] * 10 ** 9)  # we canonically calculate frequency as log occurrences/1 billion words
                self.words.append(distractor(word, freq))

    def in_dict(self, test_word):
        """Test to see if word is in dictionary"""
        for word in self.words:
            if word.text == test_word:
                return word
        return False

    def get_words(self, length_low, length_high, freq_low, freq_high):
        """Returns a list of words within specified ranges"""
        matches = []
        for word in self.words:
            if freq_low <= word.freq <= freq_high and length_low <= word.len <= length_high:
                matches.append(word.text)
        return matches

    def get_potential_distractors(self, min_length, max_length, min_freq, max_freq, params):
        """returns list of n words, if possible from between threshold values
        if not tries things nearby -- higher frequency and then lower"""
        distractor_opts = self.get_words(min_length, max_length, min_freq, max_freq)
        random.shuffle(distractor_opts)
        n=params['num_to_test']
        if len(distractor_opts) >= n:
            return distractor_opts[:n]
        else:
            logging.info("Having to widen distractor option search")
            still_need = n - len(distractor_opts)
            i = 1
            while i < 10:
                new = []
                lower = self.get_words(min_length, max_length, min_freq - i, min_freq - i + 1)
                higher = self.get_words(min_length, max_length, max_freq + i - 1, max_freq + i)
                new.extend(lower)
                new.extend(higher)
                random.shuffle(new)
                if len(new) >= still_need:
                    distractor_opts.extend(new)
                    return distractor_opts[:n]
                distractor_opts.extend(new)
                i += 1
        logging.warning("Could not find enough distractors")
        return distractor_opts


def get_frequency(word):
    """"returns frequency aligned with wf dictionary"""
    return wordfreq.zipf_frequency(word, 'en') * math.log(10)  # rescale to fit


def get_thresholds(words):
    """given words, returns min and max length to use"""
    lengths = []
    freqs = []
    for word in words:
        stripped = utils.strip_punct(word)
        lengths.append(len(stripped))
        freqs.append(get_frequency(stripped))
    min_length = min(min(lengths), 15)
    max_length = max(max(lengths), 4)
    min_freq = min(min(freqs), 11)
    max_freq = max(max(freqs), 3)
    return min_length, max_length, min_freq, max_freq

#
