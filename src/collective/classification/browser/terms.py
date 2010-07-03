from collective.classification.interfaces import IClassifiable
from zope.component import getUtility
from Products.Five.browser import BrowserView


class TermsView(BrowserView):
    """A view displaying the most important terms of the content item
    """

    def __init__(self, context, request):
        super(TermsView, self).__init__(context, request)
        path = "/".join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog
        self.brain = catalog.unrestrictedSearchResults(path=path, depth=0)[0]

    def nounTerms(self):
        """Returns the noun terms
        """
        return self.brain.noun_terms

    def npTerms(self):
        """Returns the noun-phrase terms
        """
        return self.brain.noun_phrase_terms
