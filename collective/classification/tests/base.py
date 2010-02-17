from Products.PloneTestCase import PloneTestCase
from Products.Five.testbrowser import Browser
from collective.classification.tests.layer import ClassificationLayer
        
PloneTestCase.setupPloneSite()
        
class ClassificationTestCase(PloneTestCase.PloneTestCase):
    """We use this base class for all the tests in this package.
    """
    layer = ClassificationLayer

class ClassificationFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """For functional tests.
    """
    layer = ClassificationLayer

    def getCredentials(self):
        return '%s:%s' % (PloneTestCase.default_user,
            PloneTestCase.default_password)

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            auth = 'Basic %s' % self.getCredentials()
            browser.addHeader('Authorization', auth)
        return browser
