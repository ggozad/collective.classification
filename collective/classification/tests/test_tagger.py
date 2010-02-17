from zope.component import getUtility

from collective.classification.interfaces import IPOSTagger, ITokenizer
from collective.classification.tests.base import ClassificationTestCase
from nltk.corpus import brown


class TestTaggers(ClassificationTestCase):
    """Test the two taggers we include in the package, the n-gram tagger and 
    the Pen TreeBank. The n-gram tagger is tested after having been trained 
    with the 'news' section of the brown corpus. 
    """
    
    def setUp(self):
        """Setup the tokenized test text and select the training set for the 
        n-gram tagger.
        """
        tokenizer = getUtility(ITokenizer,
            name="collective.classification.tokenizers.NLTKTokenizer")
        text = "The quick brown fox jumped over the lazy dog."
        self.tokens = tokenizer.tokenize(text)
        self.tagged_sents = brown.tagged_sents(categories='news')
        
    def test_ngram_tagger(self):
        """Tests the n-gram tagger.
        """
        tagger = getUtility(IPOSTagger,
            name="collective.classification.taggers.NgramTagger")
        tagger.train(self.tagged_sents)

        self.failUnless(tagger.tag(self.tokens) == 
            [('The', 'AT'), ('quick', 'JJ'), ('brown', 'NN'), ('fox', 'NN'), 
             ('jumped', 'VBD'), ('over', 'RP'), ('the', 'AT'), ('lazy', 'JJ'), 
             ('dog', 'NN'), ('.', '.')])
                      
    def test_pentreebank_tagger(self):
        """Tests the Pen TreeBank tagger.
        """
        tagger = getUtility(IPOSTagger,
            name="collective.classification.taggers.PennTreebankTagger")

        self.failUnless(tagger.tag(self.tokens) == 
            [('The', 'DT'), ('quick', 'NN'), ('brown', 'NN'), ('fox', 'NN'), 
             ('jumped', 'VBD'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'NN'), 
             ('dog', 'NN'), ('.', '.')])

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTaggers))
    return suite
