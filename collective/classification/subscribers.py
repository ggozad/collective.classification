from zope.component import getUtility
from plone.intelligenttext.transforms \
    import convertHtmlToWebIntelligentPlainText

from collective.classification.interfaces import IContentClassifier
from collective.classification.interfaces import INounPhraseStorage
from zope.component.interfaces import ComponentLookupError

def updateClassifier(obj,event):

    try:
        termstorage = getUtility(INounPhraseStorage)    
        classifier = getUtility(IContentClassifier)
    except ComponentLookupError:
        return
    uid = obj.UID()
    text = convertHtmlToWebIntelligentPlainText(
        obj.SearchableText())
    termstorage.addDocument(uid,text)
    subjects = obj.Subject()
    
    if subjects:
        classifier = getUtility(IContentClassifier)
        classifier.addTrainingDocument(uid,subjects)
        if classifier.trainAfterUpdate:
            classifier.train()