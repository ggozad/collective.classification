from operator import itemgetter
from zope.component import getUtility
from collective.classification.tests.base import ClassificationTestCase
from collective.classification.tests.util import readData
from collective.classification.interfaces import ITermExtractor

class TestExtractor(ClassificationTestCase):
    """Tests the Noun-phrase term extractor. Reads a review of Alice in 
    Wonderland and extracts the most frequent nouns found in the text as well 
    as the most frequent 'noun phrases'.
    """
    def test_extractor(self):
        """Reads a review of Alice in Wonderland and extracts the most
        frequent nouns found in the text as well as the most frequent 
        'noun phrases'.
        """
        
        text = readData('alicereview.txt')
        
        extractor = getUtility(ITermExtractor)
        (simple_terms,np_terms)  =  extractor.extract(text)
        important_terms = sorted(
            simple_terms.items(),
            key = itemgetter(1),
            reverse=True)[:10]
            
        self.failUnless(
            important_terms == 
            [('alice', 80), ('queen', 19), ('rabbit', 15), ('hatter', 13),
            ('door', 13), ('cat', 13), ('chapter', 12), ('king', 12),
            ('turtle', 11), ('duchess', 11)])

        important_np_terms = sorted(
            np_terms.items(),
            key = itemgetter(1),
            reverse=True)[:10]
               
        self.failUnless(
            important_np_terms == 
            [('white rabbit', 8), ('mock turtle', 8), ('cheshire cat', 5),
             ('march hare', 4), ('mad hatter', 3)]
            )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestExtractor))
    return suite
