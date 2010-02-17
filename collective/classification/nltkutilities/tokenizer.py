from zope.interface import implements
from nltk import word_tokenize, sent_tokenize

from collective.classification.interfaces import ITokenizer

class NLTKTokenizer(object):
    """Tokenizes text using the default nltk tokenizer
    """
    
    implements(ITokenizer)
    
    def tokenize(self,text):
        """
        """
        sentences = sent_tokenize(text)
        tokens = []
        for sentence in sentences:
            tokens = tokens + word_tokenize(sentence)
        return tokens