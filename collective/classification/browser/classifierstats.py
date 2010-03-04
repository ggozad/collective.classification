from collective.classification.interfaces import IContentClassifier
from zope.component import getUtility
from Products.Five.browser import BrowserView

class ClassifierStatsView(BrowserView):
    """A view displaying classifier statistics
    """
        
    def documentsParsed(self):
        """
        """
        return 
    def informativeFeatures(self):
        """
        """
        classifier = getUtility(IContentClassifier)
        return classifier.informativeFeatures(50)