from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from collective.classification.tests.base import ClassificationTestCase
from collective.classification.interfaces import IContentClassifier


class TestSubscribers(ClassificationTestCase):
    """Tests the subscribers
    """

    def test_subscribers(self):
        """Creates, modifies and deletes a document in order to test the
        subscribers.
        """

        classifier = getUtility(IContentClassifier)
        text = """
        This is a boring test. A boring test? Yes a boring test!
        """
        #Let's create a document. This has enough text to be added to the
        # catalog, and a subject so it will be added to the classifier.
        self.folder.invokeFactory('Document', 'test',
                                  title="test",
                                  text=text,
                                  subject="A Subject")
        self.failUnless(classifier.classifier is not None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSubscribers))
    return suite
