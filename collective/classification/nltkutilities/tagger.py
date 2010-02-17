from zope.interface import implements
from nltk import pos_tag
from nltk import AffixTagger, UnigramTagger, BigramTagger, \
    TrigramTagger, DefaultTagger


from collective.classification.interfaces import IPOSTagger

class PennTreebankTagger(object):
    """Tokenizes text using the default nltk tagger, based on Penn Treebank
    """
    
    implements(IPOSTagger)
    def train(self,sentence_list):
        pass
    
    def tag(self,words):
        """
        """
        return pos_tag(words)

class NgramTagger(object):
    """ Trigram tagger
    """
    
    def __init__(self):
        self.tagger = None
    
    def train(self,sentence_list):
        """
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
    
    def tag(self,words):
        """
        """
        if not self.tagger:
            raise Exception("Trigram Tagger not trained.")
        return self.tagger.tag(words)
            
            
            