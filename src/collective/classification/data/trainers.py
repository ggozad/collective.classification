import pickle
from collective.classification.taggers.taggers import BrillTrigramTagger

def dump(tagger,filename):
    try:
        f = open(filename,"w")
        pickle.dump(tagger,f)
    finally:
        f.close()

def english():
    """
    """
    from collective.classification.data.downloader import \
        downloadNLTKConll2000Corpus
    downloadNLTKConll2000Corpus()
    from nltk.corpus import conll2000
    conll2000_sents = conll2000.tagged_sents()
    tagger = BrillTrigramTagger()
    tagger.train(conll2000_sents)
    dump(tagger.tagger,"english_tagger.pickle")