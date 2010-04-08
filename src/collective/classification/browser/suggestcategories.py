from base64 import b64encode
from zope.interface import Interface, implements
from zope.component import getUtility, getMultiAdapter
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.formlib import form
from plone.app.form.interfaces import IPlonePageForm
from Products.Five.formlib import formbase
from Products.statusmessages.interfaces import IStatusMessage
from collective.classification.interfaces import IContentClassifier, \
    IClassifiable
from collective.classification import ClassificationMessageFactory as _

class ISuggestCategories(Interface):
    """
    """
    suggestions = schema.List(
        title = _(u"Suggestions"),
        description = _(u""),
        default = []
    )

class SuggestCategoriesView(formbase.PageForm):
    """Suggest categories to the user and let him set them.
    """

    implements(IPlonePageForm)
    label = _(u"Suggested categories")
    description = _(u"Choose among the proposed subjects. Clicking on apply "\
        "will add the chosen categories to the existing ones.")

    def getSuggestedSubjects(self):
        """
        """
        classifier = getUtility(IContentClassifier)
        uid = IClassifiable(self.context).UID
        return classifier.probabilityClassify(uid)

    @property
    def form_fields(self):
        """
        """
        ff = form.Fields(ISuggestCategories)
        suggestions = self.getSuggestedSubjects()
        subject_prob_list = [
            (suggestions.prob(subject),subject)
            for subject in suggestions.samples()
        ]
        subject_prob_list = sorted(subject_prob_list,reverse=True)
        vocab_terms = []
        for (probability,subject) in subject_prob_list:
            label = "%s %2.1f%%"%(subject,probability*100)
            vocab_terms.append(SimpleTerm(value=subject,
                                          token=b64encode(subject),
                                          title=label))
        choice = schema.Choice(vocabulary=SimpleVocabulary(vocab_terms))
        ff['suggestions'].field.value_type = choice
        return ff

    @form.action(_(u"Apply"))
    def action_submit(self, action, data):
        """
        """
        obj = IClassifiable(self.context)
        subjects = obj.categories
        for subject in data['suggestions']:
            if subject not in subjects:
                subjects.append(subject)
        obj.categories = subjects
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        IStatusMessage(self.request).addStatusMessage(
            _(u"Categories saved."),type="info")
        self.request.response.redirect(url)
        return ''