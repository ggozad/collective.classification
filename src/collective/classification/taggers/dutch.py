import pickle
from os.path import dirname, join
from zope.interface import implements
import nltk
from collective.classification.interfaces import IPOSTagger, ITokenizer
from collective.classification.taggers.tokenizers import Tokenizer
from collective.classification import data


class DutchTokenizer(Tokenizer):
    """Tokenizes text using the default nltk tokenizer (dutch)
    """

    implements(ITokenizer)

    def __init__(self):
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/dutch.pickle')

dutch_tokenizer = DutchTokenizer()


class DutchTagger(object):
    """ Brill/Trigram/Affix tagger (dutch)
    """
    implements(IPOSTagger)

    np_grammar = nltk.RegexpParser("NP: {<ADJ>*<N.*>+}")

    def __init__(self):
        filename = join(dirname(data.__file__), 'dutch_tagger.pickle')
        try:
            f = open(filename, 'r')
            self.tagger = pickle.load(f)
        finally:
            f.close()

    def tag(self, words):
        """
        """
        return self.tagger.tag(words)

    def normalize(self, term, tag):
        """
        """
        return term

dutch_tagger = DutchTagger()
