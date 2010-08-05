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
        (simple_terms, np_terms) = extractor.extract(text, locale="en")

        top_5_nouns = sorted(
            simple_terms.items(),
            key = itemgetter(1),
            reverse=True)[:5]
        top_5_nouns = [term for (term, rank) in top_5_nouns]
        for word in ['alice', 'rabbit', 'hatter', 'door', 'cat']:
            self.failUnless(word in top_5_nouns)

        top_5_nps = sorted(
            np_terms.items(),
            key = itemgetter(1),
            reverse=True)[:5]
        top_5_nps = [term for (term, rank) in top_5_nps]
        for np in ['white rabbit', 'mock turtle', 'mad hatter', 'march hare']:
            self.failUnless(np in top_5_nps)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestExtractor))
    return suite
