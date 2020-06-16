import logging

class Repeatcounter:
    """Keeps track of how many times each distractor has been used so far in the entire set of all items.
    Provides a list of those that are now banned b/c they have been used too much, and counts the rest.
    Disallows more than max number. If max is 0, no max is enforced."""

    def __init__(self,max):
        """initializes counter"""
        self.max=max
        if max==0:
            self.limit=False
        else:
            self.limit=True
        self.distractors=dict()
        self.banned=[]

    def increment(self, word):
        """adds a new repeat of word to the list, if this puts it up to max, adds it to banned"""
        if word in self.distractors.keys():
            self.distractors[word]+=1
        else:
            self.distractors[word]=1
        if self.limit:
            if self.distractors[word]>=self.max:
                self.banned.append(word)
