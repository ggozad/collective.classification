from zope.interface import implements, Interface
from zope import schema
from zope.component import adapts, getUtility, getMultiAdapter
from zope.formlib import form
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from collective.classification.interfaces import IContentClassifier
from collective.classification import ClassificationMessageFactory as _


class IClassifierSettingsSchema(Interface):
    """Classifier settings
    """

    train_after_update = schema.Bool(
        title=_(u"Train after update"),
        description=_(u"Enabling this will trigger training the classifier " \
            "every time tagged content is added, modified or deleted. " \
            "Disabling it means you will have to periodically manually " \
            "retrain the classifier."))


class ClassifierSettingsAdapter(SchemaAdapterBase):
    """TODO: Fill in the properties that 'pass' saving and retrieving tagger
    properties
    """
    adapts(IPloneSiteRoot)
    implements(IClassifierSettingsSchema)

    def __init__(self, context):
        super(ClassifierSettingsAdapter, self).__init__(context)
        self.classifier = getUtility(IContentClassifier)

    def get_train_after_update(self):
        return self.classifier.trainAfterUpdate

    def set_train_after_update(self, train_after_update):
        self.classifier.trainAfterUpdate = train_after_update

    train_after_update = property(get_train_after_update,
                                  set_train_after_update)


class ClassifierSettings(ControlPanelForm):

    form_fields = form.FormFields(IClassifierSettingsSchema)
    label = _("Classification settings")
    description = _("Settings for collective.classification.")
    form_name = _("Classification settings")

    @form.action(_(u"Save"))
    def save_action(self, action, data):
        form.applyChanges(self.context, self.form_fields, data, self.adapters)
        self.status = _(u"Changes saved.")

    @form.action(_(u"Retrain classifier"))
    def retrain_classifier_action(self, action, data):
        classifier = getUtility(IContentClassifier)
        classifier.train()
        self.status = _(u"Classifier trained.")

    @form.action(_(u"Statistics"), validator=null_validator)
    def stats_action(self, action, data):
        """Displays the stats view.
        """
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/@@classification-stats')
        return ''

    @form.action(_(u"Cancel"), validator=null_validator)
    def cancel_action(self, action, data):
        self.status = _(u"Changes cancelled.")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''
