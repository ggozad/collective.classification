from zope.interface import implements,Interface
from zope.component import adapts, getUtility, getMultiAdapter
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.formlib import form
from zope import schema
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator
from plone.intelligenttext.transforms import \
    convertHtmlToWebIntelligentPlainText
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFCore.utils import getToolByName
from collective.classification.interfaces import IContentClassifier, \
    INounPhraseStorage
from collective.classification import ClassificationMessageFactory as _


class IClassifierSettingsSchema(Interface):
    """Classifier settings
    """
    no_noun_ranks = schema.Int(
        title=_(u"Important nouns to keep"),
        description=_(u"Indicates how many nouns to keep when building the" \
            "list of most frequent nouns in the text."),
        default=20,
        required=True
    )

    train_after_update = schema.Bool(
        title=_(u"Train after update"),
        description=_(u"Enabling this will trigger training the classifier " \
            "every time tagged content is added, modified or deleted. " \
            "Disabling it means you will have to periodically manually " \
            "retrain the classifier.")
    )

    friendly_types = schema.List(
        required = False,
        title = _(u"Content types parsed"),
        description = _(u"Restrict the content types parsed. Leaving this " \
            "empty will include all user-friendly content types."),
        value_type = schema.Choice(vocabulary =
            'plone.app.vocabularies.ReallyUserFriendlyTypes'),
    )


class ClassifierSettingsAdapter(SchemaAdapterBase):
    """TODO: Fill in the properties that 'pass' saving and retrieving tagger
    properties
    """
    adapts(IPloneSiteRoot)
    implements(IClassifierSettingsSchema)

    def __init__(self, context):
        super(ClassifierSettingsAdapter, self).__init__(context)
        self.classifier = getUtility(IContentClassifier)
        self.storage = getUtility(INounPhraseStorage)

    def get_no_noun_ranks(self):
        return self.classifier.noNounRanksToKeep

    def set_no_noun_ranks(self,no_ranks):
        self.classifier.noNounRanksToKeep = no_ranks

    no_noun_ranks = property(get_no_noun_ranks,set_no_noun_ranks)

    def get_train_after_update(self):
        return self.classifier.trainAfterUpdate

    def set_train_after_update(self,train_after_update):
        self.classifier.trainAfterUpdate = train_after_update

    train_after_update = property(get_train_after_update,
                                  set_train_after_update)

    def get_friendly_types(self):
        return self.storage.friendlyTypes

    def set_friendly_types(self,friendly_types):
        self.storage.friendlyTypes = friendly_types

    friendly_types = property(get_friendly_types,
        set_friendly_types)

    def get_no_documents(self):
        return len(self.storage.rankedNouns)

    no_documents = property(get_no_documents)

class ClassifierSettings(ControlPanelForm):
    """
    """

    form_fields = form.FormFields(IClassifierSettingsSchema)

    label = _("Classification settings")
    description = _("Settings for collective.classification.")
    form_name = _("Classification settings")
    
    @form.action(_(u"Save"))
    def save_action(self,action,data):
        form.applyChanges(self.context, self.form_fields, data, self.adapters)
        self.status = _(u"Changes saved. You will need to reparse the " \
            "content and then retrain the classifier.")

    @form.action(_(u"Reparse all documents"))
    def retrain_termextractor_action(self,action,data):        
        storage = getUtility(INounPhraseStorage)
        storage.clear()

        catalog = getToolByName(self.context, 'portal_catalog')
        types_to_search = storage.friendlyTypes or \
            self._friendlyContentTypes()
        trainContent = catalog.searchResults(
            portal_type=types_to_search)
        for item in trainContent:
            # NOTE: Why can't I obtain item.SearchableText?
            # Is it too big to be returned in catalog brains?
            obj = item.getObject()
            uid = obj.UID()
            text = convertHtmlToWebIntelligentPlainText(
                obj.SearchableText())
            storage.addDocument(uid,text)
        self.status = _(u"Documents reparsed. You will need to re-train the "\
                         "classifier as well.")

    @form.action(_(u"Retrain classifier"))
    def retrain_classifier_action(self,action,data):
        storage = getUtility(INounPhraseStorage)
        classifier = getUtility(IContentClassifier)
        classifier.clear()
        catalog = getToolByName(self.context, 'portal_catalog')
        types_to_search = storage.friendlyTypes or \
            self._friendlyContentTypes()
        trainContent = catalog.searchResults(
            portal_type=types_to_search)        
        for item in trainContent:
            if item.Subject:
                classifier.addTrainingDocument(
                    item['UID'],
                    item['Subject'])
        classifier.train()
        self.status = _(u"Classifier trained.")

    @form.action(_(u"Statistics"),validator=null_validator)
    def stats_action(self,action,data):
        """Displays the stats view.
        """
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/@@classification-stats')
        return ''

    @form.action(_(u"Cancel"),validator=null_validator)
    def cancel_action(self, action, data):
        self.status = _(u"Changes cancelled.")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''

    def _friendlyContentTypes(self):
        friendlyTypesVoc = getUtility(IVocabularyFactory,
            'plone.app.vocabularies.ReallyUserFriendlyTypes')
        return [item.value for item in friendlyTypesVoc(self.context)]