from zope.interface import Interface, Attribute

class IClassifiable(Interface):
    """An interface for objects on which we can perform term extraction and
    classification.
    """

    UID = Attribute("""A unique identifier of the object.""")
    text = Attribute("""The text on which we perform term extraction.""")
    categories = Attribute("""The categories with which we train a classifier.""")
    language = Attribute("""The language of the content item.""")

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

    def extract(text,locale):
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