from base64 import b64encode
from zope.interface import Interface, implements
from zope.component import getUtility
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.formlib import form
from plone.app.form.interfaces import IPlonePageForm
from plone.intelligenttext.transforms import \
    convertHtmlToWebIntelligentPlainText
from Products.Five.formlib import formbase
from qi.kb.classification.interfaces import IContentClassifier
from qi.kb.classification import ClassificationMessageFactory as _

class ISuggestSubject(Interface):
    """
    """
    suggestions = schema.List(
        title = _(u"Suggestions"),
        description = _(u""),
        default = [] 
    )

class SubjectSuggestView(formbase.PageForm):
    """Suggest subjects to the user and let him set them.
    """
    implements(IPlonePageForm)
    label = _(u"Suggested subjects")
    description = _(u"Choose among the proposed subjects. Clicking on apply" \
        " will add the chosen subjects to the existing ones.")

    def getSuggestedSubjects(self):
        """
        """
        classifier = getUtility(IContentClassifier)
        searchable_text = convertHtmlToWebIntelligentPlainText(
            self.context.SearchableText())
        return classifier.probabilityClassify(searchable_text)

    @property
    def form_fields(self):
        """
        """
        ff = form.Fields(ISuggestSubject)
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
        subjects = list(self.context.Subject())
        for subject in data['suggestions']:
            if subject not in subjects:
                subjects.append(subject)
        self.context.setSubject(subjects)
        