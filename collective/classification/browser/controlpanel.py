from plone.intelligenttext.transforms import convertHtmlToWebIntelligentPlainText
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.formlib import form
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator
from plone.fieldsets.fieldsets import FormFieldsets
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFCore.utils import getToolByName
from collective.classification.interfaces import IContentClassifier
from collective.classification import ClassificationMessageFactory as _
from nltk.corpus import brown
from collective.classification.interfaces import IPOSTagger
from collective.classification.classifiers.npextractor import NPExtractor
from collective.classification.interfaces import INounPhraseStorage

brownCategories = SimpleVocabulary.fromValues(brown.categories())
taggers = SimpleVocabulary.fromValues(['Pen TreeBank','N-Gram'])

class IClassifierSettingsSchema(Interface):
    """Classifier settings
    """
    
    no_noun_ranks = schema.Int(
        title=_(u"Important nouns to keep"),
        description=_(u"Indicates how many nouns to keep when building the" \
            "list of most frequent nouns in the text."),
        default=20,
        required=True)
    
    train_after_update = schema.Bool(
        title=_(u"Train after update"),
        description=_(u"Enabling this will trigger training the classifier " \
            "every time tagged content is added, modified or deleted. " \
            "Disabling it means you will have to periodically manually " \
            "train the classifier.")
    )

class ITermExtractorSchema(Interface):
    """Term extractor settings
    """
    tagger_type = schema.Choice(
        title=_(u"Tagger type"),
        description=_(u"Choose the tagger type. By default the generic " \
            "Pen Treebank  is used, however the N-gram tagger is more " \
            "performant and gives better results."),
        vocabulary=taggers,
        required=True)
    
    brown_categories = schema.List(
        title=_(u"Brown corpus categories used for N-gram training"),
        description=_(u"Choose the categories among the available in the " \
            "Brown corpus that you think correspond most to your content. " \
            "Only applies if you have chosen the N-gram tagger above."),
        value_type=schema.Choice(vocabulary = brownCategories),
        required=True)

class IClassificationSchema(IClassifierSettingsSchema, ITermExtractorSchema):
    """Just a combination of IClassifierSettingsSchema and
    ITermExtractorSchema
    """

class ClassifierSettingsAdapter(SchemaAdapterBase):
    """TODO: Fill in the properties that 'pass' saving and retrieving tagger
    properties
    """
    adapts(IPloneSiteRoot)
    implements(IClassificationSchema)
    
    def __init__(self, context):
        super(ClassifierSettingsAdapter, self).__init__(context)
        self.classifier = getUtility(IContentClassifier)
    
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
    
    def get_tagger_type(self):
        return 'Pen TreeBank'
    
    def set_tagger_type(self):
        pass
    
    tagger_type = property(get_tagger_type,set_tagger_type)
    
    def set_brown_categories(self):
        pass
    
    def get_brown_categories(self):
        return ['news']
    
    brown_categories = property(get_brown_categories,set_brown_categories)

classifierset = FormFieldsets(IClassifierSettingsSchema)
classifierset.id = 'classifier'
classifierset.label = u"Classifier settings"
termextractorset = FormFieldsets(ITermExtractorSchema)
termextractorset.id = 'termextractor'
termextractorset.label = U"Term Extraction settings"

class ClassifierSettings(ControlPanelForm):
    """
    """
    
    form_fields = FormFieldsets(classifierset,termextractorset)
    
    label = _("Classifier settings")
    description = _("Settings for the content classifier.")
    form_name = _("Classifier settings")
    
    @form.action(_(u"Save"))
    def save_action(self,action,data):
        form.applyChanges(self.context, self.form_fields, data, self.adapters)
        self.status = _(u"Changes saved.")
    
    @form.action(_(u"Re-train classifier"))
    def retrain_classifier_action(self,action,data):
        form.applyChanges(self.context, self.form_fields, data, self.adapters)
        classifier = getUtility(IContentClassifier)
        classifier.clear()
        catalog = getToolByName(self.context, 'portal_catalog')
        trainContent = catalog.searchResults()
        for item in trainContent:
            if item.Subject:
                classifier.addTrainingDocument(
                    item['UID'],
                    item['Subject'])
        classifier.train()
        self.status = _(u"Classifier trained.")
    
    @form.action(_(u"Re-train term extractor"))
    def retrain_termextractor_action(self,action,data):
        tagger = None
        if data['tagger_type'] == 'N-Gram':
            tagged_sents = brown.tagged_sents(
                categories=data['brown_categories'])
            tagger = getUtility(IPOSTagger,
                name="collective.classification.taggers.NgramTagger")
            tagger.train(tagged_sents)
        else:
            tagger = getUtility(IPOSTagger,
                name="collective.classification.taggers.PennTreebankTagger")
        extractor = NPExtractor(tagger=tagger)
        storage = getUtility(INounPhraseStorage)
        storage.extractor = extractor
        storage.clear()
        catalog = getToolByName(self.context, 'portal_catalog')
        trainContent = catalog.searchResults()
        for item in trainContent:
            # NOTE: Why can't I obtain item.SearchableText?
            # Is it too big to be returned in catalog brains?
            obj = item.getObject()
            uid = obj.UID()
            text = convertHtmlToWebIntelligentPlainText(
                obj.SearchableText())
            storage.addDocument(uid,text)
        self.status = _(u"Term extractor trained and NP storage updated." \
        " You will need to re-train the classifier as well.")
    
    @form.action(_(u"Cancel"),validator=null_validator)
    def cancel_action(self, action, data):
        self.status = _(u"Changes cancelled.")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''