from zope.component import queryUtility, queryAdapter
from collective.classification.interfaces import IContentClassifier,\
    IClassifiable


def _wrapClassifiable(obj):
    """Looks whether the object is adaptable to IClassifiable,
    and returns the wrapper"""

    if not IClassifiable.providedBy(obj):
        wrapper = queryAdapter(obj, IClassifiable)
        if wrapper:
            obj = wrapper
        else:
            return None
    return obj


def updateClassifier(event):
    """
    """
    classifier = queryUtility(IContentClassifier)
    if not classifier:
        return

    obj = _wrapClassifiable(event.object)
    # If it is not IClassifiable abort
    if not obj:
        return
    # If it is AT-based check if blackilisted
    if classifier.trainAfterUpdate:
        classifier.train()
