from Products.CMFCore.utils import getToolByName
from collective.classification.tests.util import readData
from collective.classification.tests.base import ClassificationTestCase


class TestIndexer(ClassificationTestCase):
    """Tests the adapters for IATContentType
    """

    def test_indexer(self):
        """Creates an IATContentType and tests the catalog index
        """
        text = readData('alicereview.txt')
        self.folder.invokeFactory('Document', 'test',
                                  text=text,
                                  subject="A Subject")
        catalog = getToolByName(self.folder, 'portal_catalog')
        cr = catalog.searchResults(noun_terms="alice")
        self.failUnless(cr[0]['noun_terms'][:5] ==
            ['alice', 'rabbit', 'door', 'cat', 'hatter'])
        self.failUnless(cr[0]['noun_phrase_terms'][:5] ==
            ['mock turtle', 'white rabbit', 'march hare', 'mad hatter'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestIndexer))
    return suite
