import gensim
from nltk.corpus import brown
model = gensim.models.Word2Vec.load('brown.embedding')
model = gensim.models.Word2Vec(brown.sents())
model.save('brown.embedding')

def match(sentence_set):
