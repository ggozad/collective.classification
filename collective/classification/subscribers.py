from zope.component import getUtility
from collective.classification.interfaces import IContentClassifier, IClassifiable
from collective.classification.interfaces import INounPhraseStorage
from zope.component.interfaces import ComponentLookupError

def updateClassifier(obj,event):

    try:
        termstorage = getUtility(INounPhraseStorage)    
        classifier = getUtility(IContentClassifier)
    except ComponentLookupError:
        # The local utilites have not been registered, so what's the point?
        return
    if not termstorage.friendlyTypes or \
        obj.portal_type in termstorage.friendlyTypes:
        obj = IClassifiable(obj)
        uid = obj.UID
        text = obj.text
        termstorage.addDocument(uid,text)
        subjects = obj.categories
        classifier.addTrainingDocument(uid,subjects)
        if classifier.trainAfterUpdate:
            classifier.train()

def removeFromClassifier(obj,event):
    try:
        termstorage = getUtility(INounPhraseStorage)    
        classifier = getUtility(IContentClassifier)
    except ComponentLookupError:
        # The local utilites have not been registered, so what's the point?
        return
    obj = IClassifiable(obj)    
    classifier.removeTrainingDocument(obj.UID)
    termstorage.removeDocument(obj.UID)