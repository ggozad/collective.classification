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
    
    def UID(self):
        return self.context.UID()
    
    def text(self):
        """
        """
        return convertHtmlToWebIntelligentPlainText(
            self.context.SearchableText())
    
    def keywords(self):
        """
        """
        return self.context.Subject()
