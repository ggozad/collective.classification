from Products.Five.formlib import formbase
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import Interface
from collective.classification.interfaces import IContentClassifier
from zope.component import getUtility
from collective.classification import ClassificationMessageFactory as _

class IStats(Interface):
    """
    """
    
    no_features = schema.Int(
        title = _(u"Number of important features to show"),
        description = _(u""),
        required = True,
        default = 10
    )
    
class ClassifierStatsView(formbase.PageForm):
    """
    """

    form_fields = form.Fields(IStats)
    template = ViewPageTemplateFile('classifierstats.pt')

    def __init__(self, *args, **kwargs):
        """
        """
        super(ClassifierStatsView,self).__init__(*args,**kwargs)
        self.classifier = getUtility(IContentClassifier)
        self.informativeFeatures = self.classifier.informativeFeatures()
        
        
    
    @form.action(_(u"Apply"))
    def action_apply(self, action, data):
        """
        """
        self.informativeFeatures = \
            self.classifier.informativeFeatures(data['no_features'])
