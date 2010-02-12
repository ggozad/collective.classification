from zope.interface import Interface

class ITokenizer(Interface):
    """
    """
    
    def tokenize(text):
        """Tokenizes the text
        
        Returns the list of tokens
        """

class IPOSTagger(Interface):
    """Interface of Parts Of Speech taggers.
    """
    def train(tagged_sentences):
        """Trains the tagger if necessary. Tagged sentences is a list of
        sentences where each sentence is a list of tuples of the form
        (word,tag)
        """
    
    def tag(tokens):
        """Characterizes words as POS.
        
        Returns a list of tuples (word,POS)
        """

class ITermExtractor(Interface):
    """Interface for term extractors
    """
    
    def extract(text):
        """Extracts terms from text.
        """

class INounPhraseStorage(Interface):
    """
    """


class IContentClassifier(Interface):
    """Interface for classifiers
    """

class IContentClusterer(Interface):
    """Interface for clusterers
    """

