from zope.component import getUtility, queryAdapter
from zope.component.interfaces import ComponentLookupError
from Products.ATContentTypes.interface import IATContentType
from collective.classification.interfaces import IContentClassifier, IClassifiable
from collective.classification.interfaces import INounPhraseStorage

def _wrapClassifiable(obj):
    """Looks whether the object is adaptable to IClassifiable,
    and returns the wrapper"""

    if not IClassifiable.providedBy(obj):
        wrapper = queryAdapter(obj,IClassifiable)
        if wrapper:
            obj = wrapper
        else:
            return None
    return obj

def updateClassifier(event):
    """
    """
    try:
        termstorage = getUtility(INounPhraseStorage)    
        classifier = getUtility(IContentClassifier)
    except ComponentLookupError:
        # The local utilites have not been registered, so what's the point?
        return

    obj = _wrapClassifiable(event.object)    
    # If it is not IClassifiable abort
    if not obj:
        return
    # If it is AT-based check if blackilisted
    if IATContentType.providedBy(event.object) and \
        termstorage.friendlyTypes and \
        event.object.portal_type not in termstorage.friendlyTypes:
        return    
    uid = obj.UID
    text = obj.text
    locale = obj.language
    termstorage.addDocument(uid,text)
    subjects = obj.categories
    classifier.addTrainingDocument(uid,subjects)
    if classifier.trainAfterUpdate:
        classifier.train()

def removeFromClassifier(event):
    try:
        termstorage = getUtility(INounPhraseStorage)    
        classifier = getUtility(IContentClassifier)
    except ComponentLookupError:
        # The local utilites have not been registered, so what's the point?
        return
    obj = _wrapClassifiable(event.object)
    # If it is not IClassifiable abort
    if not obj:
        return
    classifier.removeTrainingDocument(obj.UID)
    termstorage.removeDocument(obj.UID)