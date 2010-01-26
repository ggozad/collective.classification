from qi.kb.classification.interfaces import IContentClassifier
from zope.component import getUtility
from plone.intelligenttext.transforms \
    import convertHtmlToWebIntelligentPlainText

def updateClassifier(obj,event):
    subjects = obj.Subject()
    if subjects:
        uid = obj.UID()
        text = convertHtmlToWebIntelligentPlainText(
            obj.SearchableText())
        classifier = getUtility(IContentClassifier)
        classifier.addTrainingDocument(uid,text,subjects)
        if classifier.trainAfterUpdate:
            classifier.train()