import pickle
from os.path import dirname, join
from zope.interface import implements
import nltk
from collective.classification.interfaces import IPOSTagger, ITokenizer
from collective.classification import data

class EnglishTokenizer(object):
    """Tokenizes text using the default nltk tokenizer
    """
    implements(ITokenizer)
    def __init__(self):
        self.sent_tokenizer = nltk.data.load(
            'tokenizers/punkt/english.pickle')
    def tokenize(self,text):
        """
        """
        sentences = self.sent_tokenizer.tokenize(text)
        tokens = []
        for sentence in sentences:
            tokens = tokens + nltk.word_tokenize(sentence)
        return tokens

english_tokenizer = EnglishTokenizer()

class EnglishTagger(object):
    """ Brill/Trigram/Affix tagger
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


english_tagger = EnglishTagger()
