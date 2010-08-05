from zope.interface import Interface, Attribute


class IClassifiable(Interface):
    """An interface for objects on which we can perform term extraction and
    classification.
    """

    UID = Attribute("""A unique identifier of the object.""")
    text = Attribute("""The text on which we perform term extraction.""")
    categories = Attribute(
        """The categories with which we train a classifier.""")
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

    np_grammar = Attribute(
        """A regular expression for Noun-phraseidentification""")

    def tag(tokens):
        """Characterizes words as POS.
        Returns a list of tuples (word,POS)
        """

    def normalize(term, tag):
        """Return the normal form of a word if appropriate.
        """


class ITermExtractor(Interface):
    """Interface for term extractors
    """

    def extract(text, locale):
        """Extracts terms from text.
        """


class IContentClassifier(Interface):
    """Interface for classifiers
    """


class IContentClusterer(Interface):
    """Interface for clusterers
    """


class ISimilarFinder(Interface):
    """Interface for utilities finding similar items
    """
