import pickle
from collective.classification.taggers.taggers import BrillTrigramTagger


def dump(tagger, filename):
    try:
        f = open(filename, "w")
        pickle.dump(tagger, f)
    finally:
        f.close()


def english():
    from collective.classification.data.downloader import\
        downloadNLTKConll2000Corpus
    downloadNLTKConll2000Corpus()
    from nltk.corpus import conll2000
    conll2000_sents = conll2000.tagged_sents()
    tagger = BrillTrigramTagger()
    tagger.train(conll2000_sents)
    dump(tagger.tagger, "english_tagger.pickle")


def dutch():
    from collective.classification.data.downloader import\
        downloadNLTKAlpinoCorpus
    downloadNLTKAlpinoCorpus()
    from nltk.corpus import alpino
    alpino_sents = alpino.tagged_sents(simplify_tags=True)
    tagger = BrillTrigramTagger()
    tagger.train(alpino_sents)
    dump(tagger.tagger, "dutch_tagger.pickle")

def romanian():
    from collective.classification.data.downloader import\
        downloadNLTKEurParlRaw
    downloadNLTKEurParlRaw()
    from nltk.corpus import europarl_raw
    europarl_sents = europarl_raw.romanian.sents()
    tagger = BrillTrigramTagger()
    tagger.train(europarl_sents)
    dump(tagger.tagger, "romanian_tagger.pickle")
