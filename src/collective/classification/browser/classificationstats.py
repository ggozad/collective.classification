from zope.interface import Interface
from zope.component import getUtility
from zope import schema
from zope.formlib import form
from Products.Five.formlib import formbase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from collective.classification.interfaces import IContentClassifier
from collective.classification import ClassificationMessageFactory as _


class IStats(Interface):
    no_features = schema.Int(
        title=_(u"Number of informative features to show"),
        required=True,
        default=10)


class ClassificationStatsView(formbase.PageForm):
    form_fields = form.Fields(IStats)
    template = ViewPageTemplateFile('classificationstats.pt')

    def __init__(self, *args, **kwargs):
        """
        """
        super(ClassificationStatsView, self).__init__(*args,**kwargs)
        catalog = getToolByName(self.context, 'portal_catalog')
        self.classifier = getUtility(IContentClassifier)
        self.informativeFeatures = self.classifier.informativeFeatures()
        self.parsedDocs = len(catalog._catalog.getIndex('noun_terms')._unindex)

    @form.action(_(u"Apply"))
    def action_apply(self, action, data):
        """
        """
        self.informativeFeatures = \
            self.classifier.informativeFeatures(data['no_features'])
