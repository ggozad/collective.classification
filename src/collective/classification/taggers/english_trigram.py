import pickle
from os.path import dirname, join
from zope.interface import implements
from collective.classification.interfaces import IPOSTagger
from collective.classification import data


class TriGramTagger(object):
    """ Trigram tagger
    """
    implements(IPOSTagger)

    def __init__(self):
        filename = join(dirname(data.__file__), 'english_tagger.pickle')
        try:
            f = open(filename, 'r')
            self.tagger = pickle.load(f)
        finally:
            f.close()

    def tag(self,words):
        """
        """
        return self.tagger.tag(words)

english_trigram_tagger = TriGramTagger()
