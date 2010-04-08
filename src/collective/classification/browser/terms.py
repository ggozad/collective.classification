from collective.classification.interfaces import IClassifiable
from zope.component import getUtility
from Products.Five.browser import BrowserView
from collective.classification.interfaces import INounPhraseStorage

class TermsView(BrowserView):
    """A view displaying the most important terms of the content item
    """

    def __init__(self,context,request):
        super(TermsView,self).__init__(context,request)
        self.npstorage = getUtility(INounPhraseStorage)
        self.content_uid = IClassifiable(self.context).UID

    def nounTerms(self):
        """Returns the noun terms
        """
        return self.npstorage.getRankedNounTerms(self.content_uid)

    def npTerms(self):
        """Returns the noun-phrase terms
        """
        return self.npstorage.getRankedNPTerms(self.content_uid)
        