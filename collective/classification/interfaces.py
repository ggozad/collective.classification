from zope.interface import Interface

class IClassifiable(Interface):
    """An interface for objects on which we can perform term extraction and
    classification.
    """
    def UID():
        """Return a unique id that will be used as an identifier of the 
        object.
        """
        
    def text():
        """Return the text on which we perform term extraction.
        """
    
    def keywords():
        """Returns the keywords with which we train a classifier.
        """

class ITokenizer(Interface):
    """Marker interface for tokenizers.
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
    """Marker interface for our noun-phrase storage.
    """


class IContentClassifier(Interface):
    """Interface for classifiers
    """

class IContentClusterer(Interface):
    """Interface for clusterers
    """
