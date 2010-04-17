from collective.classification.interfaces import IContentClassifier
from collective.classification.interfaces import INounPhraseStorage
from zope.component import getUtility
from collective.classification.tests.base import ClassificationTestCase

class TestSubscribers(ClassificationTestCase):
    """Tests the subscribers
    """
    def test_subscribers(self):
        """Creates, modifies and deletes a document in order to test the
        subscribers.
        """
        npstorage = getUtility(INounPhraseStorage)
        classifier = getUtility(IContentClassifier)
        text = """
        This is a boring test. A boring test? Yes a boring test!
        """
        #Let's create a document. This has enough text to be added to the 
        # storage, and a subject so it will be added to the classifier.
        self.folder.invokeFactory('Document','test',
                                  title="test",
                                  text=text,
                                  subject="A Subject")
        self.failUnless(len(npstorage.rankedNouns) == 1)
        self.failUnless(len(classifier.trainingDocs) == 1)
        # XXX Why will this not work?
        # Now, let's remove the subject
        # self.folder['test'].edit(text="asdasd",subject="")
        # self.failUnless(len(classifier.trainingDocs) == 0)
        del self.folder['test']
        self.failUnless(len(npstorage.rankedNouns) == 0)
        self.failUnless(len(classifier.trainingDocs) == 0)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSubscribers))
    return suite
