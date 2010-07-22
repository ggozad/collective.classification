from Products.Five.browser import BrowserView
from collective.classification.classifiers.similarity import JaccardSimilarity


class SimilarItemsView(BrowserView):
    """A view displaying the most similar items to the content
    """

    def __init__(self, context, request):
        super(SimilarItemsView, self).__init__(context, request)
        self.catalog = self.context.portal_catalog

    def similar(self):
        similar = JaccardSimilarity().similar(self.context)
        result = [(self.catalog.unrestrictedSearchResults(UID=uid)[0], rel)
            for (uid, rel) in similar]
        return result
