from operator import itemgetter
from zope.interface import implements
from zope.component import adapts, getUtility
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog
from Products.ATContentTypes.interface import IATContentType
from collective.classification.interfaces import IClassifiable, ITermExtractor


class NounTermIndexer(object):
    """Index the noun terms of an object
    """

    implements(IIndexer)
    adapts(IATContentType, IZCatalog)

    def __init__(self, context, catalog):
        self.context = context
        self.catalog = catalog

    def __call__(self):
        obj = IClassifiable(self.context)
        text = obj.text
        locale = obj.language

        extractor = getUtility(ITermExtractor)
        (simple_terms, np_terms) = extractor.extract(text, locale)

        noun_scores = sorted(simple_terms.items(),
                             key = itemgetter(1),
                             reverse=True)
        return [noun for (noun, rank) in noun_scores]

class NounPhraseTermIndexer(object):
    """Index the noun phrase terms of an object
    """

    implements(IIndexer)
    adapts(IATContentType, IZCatalog)

    def __init__(self, context, catalog):
        self.context = context
        self.catalog = catalog

    def __call__(self):
        obj = IClassifiable(self.context)
        text = obj.text
        locale = obj.language

        extractor = getUtility(ITermExtractor)
        (simple_terms, np_terms) = extractor.extract(text, locale)

        np_scores = sorted(np_terms.items(),
                           key = itemgetter(1),
                           reverse=True)
        return [np for (np, rank) in np_scores]
