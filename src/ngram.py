textfile = open("CHILDES/train.txt", "r")
temp = textfile.read().splitlines()
text = [ x.split() for x in temp ]

from nltk.lm.preprocessing import padded_everygram_pipeline
train, vocab = padded_everygram_pipeline(5, text)

from nltk.lm import MLE
lm = MLE(5)
lm.fit(train, vocab)

import dill as pickle

with open('5gram-lm.pkl', 'wb') as fout:
    pickle.dump(lm, fout)

#####testing######
with open('5gram-lm.pkl', 'rb') as fin:
    model_loaded = pickle.load(fin)

lm = model_loaded

textfile = open('CHILDES/test.txt', 'r')
temp = textfile.read().splitlines()
text = [ x.split() for x in temp ]
text_unked = [ list(lm.vocab.lookup(x)) for x in text ]

from nltk.lm.preprocessing import pad_both_ends
text_padded = [ list(pad_both_ends(x, 5)) for x in text_unked ]

from nltk import ngrams
text_5grams = [ ngrams(x, 5) for x in text_padded ]

from nltk.lm.preprocessing import flatten
text_flat = flatten(text_5grams)

lm.perplexity(text_flat)

for ngram in list(text_flat):
    print(lm.perplexity([ngram]))


