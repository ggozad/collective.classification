from collective.classification.classifiers.utils import singularize
from collective.classification.tests.base import ClassificationTestCase

class TestUtilities(ClassificationTestCase):

    def test_singularization(self):
        """This is really tested elsewhere,
        see http://www.bermi.org/inflector/
        """
        self.failUnless(singularize("axes") == "axis")
        self.failUnless(singularize(":") == ":")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUtilities))
    return suite
