from operator import itemgetter
from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from collective.classification.interfaces import ISimilarFinder
from collective.classification.classifiers.utils import jaccard
from collective.classification.subscribers import _wrapClassifiable


class JaccardSimilarity(object):

    implements(ISimilarFinder)

    def similar(self, obj, noNounsToKeep=20):
        obj = _wrapClassifiable(obj)
        if obj is None:
            return []

        root = getUtility(ISiteRoot)
        catalog = getToolByName(root, 'portal_catalog')
        nounTermsIndex = catalog._catalog.getIndex('noun_terms')
        uidTermsIndex = catalog._catalog.getIndex('UID')

        cid = uidTermsIndex._index[obj.UID]
        noun_terms = nounTermsIndex._unindex[cid][:noNounsToKeep]
        similar = {}
        from BTrees.IIBTree import IITreeSet
        for term in noun_terms:
            obj_cids = nounTermsIndex._index[term]
            if not isinstance(obj_cids, IITreeSet):
                continue
            for ocid in obj_cids:
                if ocid!=cid and ocid not in similar:
                    item_nouns = nounTermsIndex._unindex[ocid][:noNounsToKeep]
                    similar[ocid] = jaccard(noun_terms, item_nouns)
        result = sorted(similar.iteritems(),
                        key=itemgetter(1),
                        reverse=True)[:5]
        return [(uidTermsIndex._unindex[cid], rel) for (cid, rel) in result]
