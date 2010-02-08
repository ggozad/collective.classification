from zope.component import getUtility
from qi.kb.classification.tests.base import ClassificationTestCase
from qi.kb.classification.classifiers.npextractor import NPExtractor
from qi.kb.classification.tests.util import readData
from qi.kb.classification.interfaces import INounPhraseStorage

from operator import itemgetter

class TestNPStorage(ClassificationTestCase):
    """Tests the Noun-phrase storage
    """
    def test_storage(self):
        """Reads a review of Alice in Wonderland and extracts the most
        frequent nouns found in the text as well as the most frequent 
        'noun phrases'.
        """
        
        text = readData('alicereview.txt')
        storage = getUtility(INounPhraseStorage)        
        storage.addDocument('alice',text)
        self.failUnless(storage.rankedNouns['alice'] == 
            [('alice', 0), ('queen', 1), ('rabbit', 2), ('hatter', 3), 
             ('door', 3), ('cat', 3), ('chapter', 6), ('king', 6), 
             ('turtle', 8), ('duchess', 8), ('hare', 10), ('table', 11), 
             ('white', 11), ('house', 13), ('mock', 13), ('time', 13), 
             ('day', 16), ('story', 16), ('mushroom', 16), ('baby', 16), 
             ('march', 20), ('caterpillar', 20), ('cheshire', 20), 
             ('sister', 20), ('size', 20), ('pool', 20), ('verdict', 26), 
             ('jury', 26), ('witness', 26), ('nothing', 26), ('side', 26), 
             ('gryphon', 26), ('head', 26), ('tea', 26), ('cook', 26), 
             ('mouse', 26), ('mad', 26), ('month', 37), ('everything', 37), 
             ('passage', 37), ('croquet', 37), ('hall', 37), ('watch', 37), 
             ('fan', 37), ('procession', 37), ('dormouse', 37), ('re', 37), 
             ('everyone', 37), ('dream', 37), ('tree', 37), ('game', 37), 
             ('window', 37), ('way', 37), ('part', 37), ('evidence', 37), 
             ('executioner', 37), ('doesn', 37), ('footman', 37)])
        
        self.failUnless(storage.rankedNPs['alice'] == 
            [('white rabbit', 0), ('mock turtle', 0), ('cheshire cat', 2), 
             ('march hare', 3), ('mad hatter', 4)])
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNPStorage))
    return suite
