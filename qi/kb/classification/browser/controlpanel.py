from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility

from zope.formlib import form
from zope import schema
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from qi.kb.classification.interfaces import IContentClassifier

from plone.app.controlpanel.form import ControlPanelForm
from qi.kb.classification import ClassificationMessageFactory as _

class IClassifierSettingsSchema(Interface):
    """Classifier settings
    """

    no_noun_ranks = schema.Int(
        title=_(u"Important nouns to keep"),
        description=_(u"The port of your XMLRPC server"),
        default=10,
        required=True)

class ClassifierSettings(ControlPanelForm):
    """
    """

    form_fields = form.FormFields(IClassifierSettingsSchema)

    label = _("Classifier settings")
    description = _("Settings for the content classifier.")
    form_name = _("Classifier settings")


class ClassifierSettingsAdapter(SchemaAdapterBase):
    """
    """
    adapts(IPloneSiteRoot)
    implements(IClassifierSettingsSchema)
    
    def __init__(self, context):
        super(ClassifierSettingsAdapter, self).__init__(context)
        self.classifer = getUtility(IContentClassifier)
    
    def get_no_noun_ranks(self):
        return self.classifer.noNounRanksToKeep
    
    def set_no_noun_ranks(self,no_ranks):
        pass
        
    no_noun_ranks = property(get_no_noun_ranks,set_no_noun_ranks)