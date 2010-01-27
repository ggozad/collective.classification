from unittest import TestSuite
from zope.testing import doctest
from Testing.ZopeTestCase import ZopeDocFileSuite
from qi.kb.classification.tests.base import ClassificationFunctionalTestCase


optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = TestSuite((
        ZopeDocFileSuite(
            'integration.txt', package='qi.kb.classification.tests',
            test_class=ClassificationFunctionalTestCase,
            optionflags=optionflags),
    ))
    return suite
