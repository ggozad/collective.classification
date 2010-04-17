from collective.classification.tests.base import ClassificationTestCase
from collective.classification.interfaces import IClassifiable
from plone.intelligenttext.transforms import convertHtmlToWebIntelligentPlainText
class TestAdapters(ClassificationTestCase):
    """Tests the adapters for IATContentType
    """
    def test_adapters(self):
        """Creates an IATContentType and tests the adaptation to IClassifiable
        """
        self.folder.invokeFactory('Document','test',
                                  text="This is a test",
                                  subject="A Subject")
        adapted = IClassifiable(self.folder['test'])
        self.failUnless(adapted.UID)
        self.failUnless(adapted.text==
            convertHtmlToWebIntelligentPlainText(
            self.folder['test'].SearchableText())
        )
        self.failUnless(adapted.categories==['A Subject'])
        self.failUnless(adapted.language == 'en')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAdapters))
    return suite
