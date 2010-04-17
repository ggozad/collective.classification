from plone.intelligenttext.transforms import convertHtmlToWebIntelligentPlainText
from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface import IATContentType
from collective.classification.interfaces import IClassifiable

class ATClassifiableAdapter(object):
    """Adapts AT-based content to IClassifiable.
    """
    implements(IClassifiable)
    adapts(IATContentType)

    def __init__(self, context):
        self.context = context

    def getUID(self):
        return self.context.UID()

    UID = property(getUID)

    def getText(self):
        """
        """
        return convertHtmlToWebIntelligentPlainText(
            self.context.SearchableText())

    text = property(getText)

    def getcategories(self):
        """
        """
        return list(self.context.Subject())

    def setcategories(self,value):
        """
        """
        return self.context.setSubject(value)    

    categories = property(getcategories,setcategories)

    def getlanguage(self):
        """
        """
        ps = self.context.unrestrictedTraverse("@@plone_portal_state")
        return self.context.Language() or ps.default_language()

    language = property(getlanguage)