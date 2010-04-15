import pickle
from nltk import AffixTagger, UnigramTagger, BigramTagger, \
    TrigramTagger, DefaultTagger
from collective.classification.interfaces import IPOSTagger

class TriGramTrainer(object):
    """ Trigram tagger trainer
    """
    def __init__(self):
        self.tagger = None

    def train(self,sentence_list):
        """Trains the tagger from the sentences ofa senten
        """
        noun_fallback = DefaultTagger('NN')
        affix_fallback = AffixTagger(sentence_list,
            backoff=noun_fallback)
        unigram_fallback = UnigramTagger(sentence_list,
            backoff=affix_fallback)
        bigram_fallback = BigramTagger(sentence_list,
            backoff=unigram_fallback)
        self.tagger = TrigramTagger(sentence_list,
            backoff=bigram_fallback)

    def dump(self,filename='trigram.pickle'):
        try:
            file = open(filename,"w")
            pickle.dump(self.tagger,file)
        finally:
            file.close()
    
def english():
    """
    """
    from nltk.corpus import conll2000
    conll2000_sents = conll2000.tagged_sents()
    trainer = TriGramTrainer()
    trainer.train(conll2000_sents)
    trainer.dump("english.pickle")