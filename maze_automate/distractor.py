import logging


class distractor:
    """General class for distractor words"""

    def __init__(self, text, freq):
        self.text = text
        self.len = len(text)
        self.freq = freq


class distractor_dict:
    """General class for distractor dictionaries"""

    def __init__(self):
        pass

    def in_dict(self, word):
        """Tests to see if word in in the dictionary"""
        pass

    def get_words(self):
        """Returns all words that meet the requirements specified in arguments"""
        pass

    def get_potential_distractors(self, n=100):
        """Returns a list of n words, if possible with required properties,
        If not, supplements with words that are 'close' to having those properties"""
        pass
