from zope.component import getUtility
from collective.classification.tests.base import ClassificationTestCase
from collective.classification.tests.util import readData
from collective.classification.interfaces import INounPhraseStorage

class TestNPStorage(ClassificationTestCase):
    """Tests the Noun-phrase storage
    """

    def test_npstorage(self):
        """Reads a review of Alice in Wonderland and extracts the most
        frequent nouns found in the text as well as the most frequent 
        'noun phrases'.
        """
        text = readData('alicereview.txt')
        storage = getUtility(INounPhraseStorage)
        storage.addDocument('alice',text)
        self.failUnless(storage.rankedNouns['alice'][:20] ==
            [('alice', 0), ('rabbit', 1), ('door', 2), ('cat', 2),
             ('hatter', 4), ('chapter', 5), ('king', 5), ('duchess', 7),
             ('table', 7), ('hare', 9), ('turtle', 10), ('white', 10),
             ('time', 10), ('mock', 13), ('house', 13), ('caterpillar', 15),
             ('day', 15), ('eats', 15), ('notice', 18), ('sister', 18)])        
        self.failUnless(storage.rankedNPs['alice'] == 
            [('mock turtle', 0), ('white rabbit', 1), ('march hare', 2), 
             ('mad hatter', 3)])
        self.failUnless(storage.getRankedTerms('alice',5) == 
            ([('alice', 0), ('rabbit', 1), ('door', 2), ('cat', 2), 
              ('hatter', 4)],
             [('mock turtle', 0), ('white rabbit', 1), ('march hare', 2),
              ('mad hatter', 3)]))
        self.failUnless(storage.getNounTerms('alice',5) == 
            ['alice', 'rabbit', 'door', 'cat', 'hatter'])
        self.failUnless(storage.getNPTerms('alice',5) == 
            ['mock turtle', 'white rabbit', 'march hare', 'mad hatter'])

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNPStorage))
    return suite