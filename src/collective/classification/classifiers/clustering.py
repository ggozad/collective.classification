import numpy
from zope.interface import implements
from zope.component import getUtility
from nltk.cluster import KMeansClusterer
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from collective.classification.classifiers.utils import pearson
from collective.classification.interfaces import IContentClusterer


class KMeans(object):
    """
    """
    implements(IContentClusterer)

    def clusterize(self, noClusters, noNounsToKeep, **kwargs):
        """
        """
        root = getUtility(ISiteRoot)
        catalog = getToolByName(root, 'portal_catalog')

        nounTermsIndex = catalog._catalog.getIndex('noun_terms')
        uidTermsIndex = catalog._catalog.getIndex('UID')
        nounTermsIndexIds = []
        allNouns = set()
        docnouns = []
        vectors = []

        for key in nounTermsIndex._unindex.keys():
            importantNouns = nounTermsIndex._unindex[key][:noNounsToKeep]
            if importantNouns:
                nounTermsIndexIds.append(key)
                docnouns.append(importantNouns)
                allNouns = allNouns.union(importantNouns)

        for nouns in docnouns:
            vector = [(noun in nouns and 1 or 0) for noun in allNouns]
            vectors.append(numpy.array(vector))

        clusterer = KMeansClusterer(noClusters, pearson, **kwargs)
        clusters = clusterer.cluster(vectors, True)
        result = {}
        for i in range(noClusters):
            result[i] = []
        for i in range(len(nounTermsIndexIds)):
            docid = nounTermsIndexIds[i]
            uid = uidTermsIndex._unindex[docid]
            result[clusters[i]] = result[clusters[i]] + [uid]

        return result
