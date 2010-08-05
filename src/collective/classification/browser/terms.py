from Products.Five.browser import BrowserView


class TermsView(BrowserView):
    """A view displaying the most important terms of the content item
    """

    def __init__(self, context, request):
        super(TermsView, self).__init__(context, request)
        catalog = self.context.portal_catalog
        results = catalog.unrestrictedSearchResults(UID=self.context.UID())
        if len(results):
            self.brain = results[0]
        else:
            self.brain = None

    def nounTerms(self):
        """Returns the noun terms
        """
        if self.brain is None:
            return []
        return self.brain.noun_terms

    def npTerms(self):
        """Returns the noun-phrase terms
        """
        if self.brain is None:
            return []
        return self.brain.noun_phrase_terms
